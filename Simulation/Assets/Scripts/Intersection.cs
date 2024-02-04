using System.Collections.Generic;
using System.Diagnostics;
using UnityEngine;

namespace TrafficSimulation{
    // Enum defining types of intersections (STOP or TRAFFIC_LIGHT)
    public enum IntersectionType{
        STOP,
        TRAFFIC_LIGHT
    }
    // a road intersection in the traffic simulation.
    public class Intersection : MonoBehaviour
    {   
        // Type of intersection
        public IntersectionType intersectionType;
        // Unique identifier for the intersection
        public int id;  

        //For stop only
        public List<Segment> prioritySegments;

        //For traffic lights only
        // Duration of green lights
        public float lightsDuration = 8;
        // Duration of orange lights
        public float orangeLightDuration = 2;
        // Segments controlled by the first group of lights
        public List<Segment> lightsNbr1;
        // Segments controlled by the second group of lights
        public List<Segment> lightsNbr2;

        // List of vehicles waiting at the intersection
        private List<GameObject> vehiclesQueue;

        // List of vehicles currently in the intersection
        private List<GameObject> vehiclesInIntersection;

        private TrafficSystem trafficSystem;

        // Current active group of red lights
        [HideInInspector] public int currentRedLightsGroup = 1;

        private Target currentTarget;

        // Time to slow down to zero speed
        public float slowingTime = 1f; 
        private float invokeTime = 5f;

        // Stopwatch for measuring intersection time
        private Stopwatch intersectionTimer;

        // Time limit for vehicles in the intersection
        private float intersectionTimeLimit = 25f;
        
        void Start(){
            vehiclesQueue = new List<GameObject>();
            vehiclesInIntersection = new List<GameObject>();
            intersectionTimer = new Stopwatch();
        }

        void Update()
        {   
            if(intersectionTimer.ElapsedMilliseconds / 1000f * Time.timeScale > intersectionTimeLimit)
            {
                UnityEngine.Debug.Log(this.name + " 's time limit reached");
                WholeProcess.playAgain = true;
            }
        }

        // Switches the traffic lights between two groups and triggers the movement of vehicles in the queue during the orange light phase.
        void SwitchLights(){

            if(currentRedLightsGroup == 1) currentRedLightsGroup = 2;
            else if(currentRedLightsGroup == 2) currentRedLightsGroup = 1;            
            
            //Wait few seconds after light transition before making the other car move (= orange light)
            Invoke("MoveVehiclesQueue", orangeLightDuration);
        }

        // Called when a vehicle enters the intersection collider.
        void OnTriggerEnter(Collider _other) {
            //Check if vehicle is already in the list if yes abort
            //Also abort if we just started the scene (if vehicles inside colliders at start)
            if(IsAlreadyInIntersection(_other.gameObject) || Time.timeSinceLevelLoad < .5f) return;

            if(_other.tag == "AutonomousVehicle" && intersectionType == IntersectionType.STOP)
            {
                TriggerStop(_other.gameObject);
            }
        }

        // Called when a vehicle exits the intersection collider.
        void OnTriggerExit(Collider _other) {
            if(_other.tag == "AutonomousVehicle" && intersectionType == IntersectionType.STOP)
                ExitStop(_other.gameObject);
            else if(_other.tag == "AutonomousVehicle" && intersectionType == IntersectionType.TRAFFIC_LIGHT)
                ExitLight(_other.gameObject);
        }

        // Triggers the stop behavior for a vehicle when it enters a stop intersection.
        void TriggerStop(GameObject _vehicle){
            VehicleAI vehicleAI = _vehicle.GetComponent<VehicleAI>();
            string vehicleAIRouteName = vehicleAI.trafficSystem.name;
            _vehicle.GetComponent<TruckInfo>().nowStatus = NowStatus.WAITING;
            

            if(!IsPrioritySegment(vehicleAIRouteName))
            {
                if(vehiclesQueue.Count > 0 || vehiclesInIntersection.Count > 0)
                {   
                    vehicleAI.vehicleStatus = Status.SLOW_DOWN;
                    vehiclesQueue.Add(_vehicle);

                    // StartCoroutine(ReduceSpeed(_vehicle));
                    vehicleAI.vehicleStatus = Status.STOP;
                    
                    if(vehiclesInIntersection.Count == 0)
                    {   
                        // Debug.Log(this.name + " checking");
                        InvokeRepeating("CheckIntersection", invokeTime, 10f);
                    }
                }

                else
                {   
                    intersectionTimer.Start();
                    vehiclesInIntersection.Add(_vehicle);
                    vehicleAI.vehicleStatus = Status.SLOW_DOWN;
                }
            }

            else
            {
                intersectionTimer.Start();
                vehicleAI.vehicleStatus = Status.SLOW_DOWN;
                vehiclesInIntersection.Add(_vehicle);
            }
        }

        // Checks the intersection to determine if waiting vehicles can proceed.
        private void CheckIntersection()
        {   
            if(vehiclesQueue.Count > 0)
            {
                int waitingVehicleCount = 0;
        
                foreach(GameObject _vehicleInQueue in vehiclesQueue)
                {   
                    if(_vehicleInQueue.GetComponent<TruckInfo>().nowStatus == NowStatus.WAITING)
                    {
                        waitingVehicleCount ++;
                    }
                }

                if(waitingVehicleCount == vehiclesQueue.Count)
                {   
                    ExitStop(vehiclesQueue[0]);
                }
            }

            else
            {
                CancelInvoke("CheckIntersection");
            }
        }

        // Reduces the speed of a vehicle to zero over a specified time.
        private System.Collections.IEnumerator ReduceSpeed(GameObject _vehicle)
        {
            Rigidbody rb = _vehicle.GetComponent<Rigidbody>();
            
            Vector3 initialVelocity = rb.velocity;
            float elapsedTime = 0f;

            while (elapsedTime < slowingTime)
            {
                rb.velocity = Vector3.Lerp(initialVelocity, Vector3.zero, elapsedTime / slowingTime);
                elapsedTime += Time.deltaTime;
                yield return null;
            }

            rb.velocity = Vector3.zero; // Ensure velocity is set to zero
        }

        // Exits the stop behavior for a vehicle when it leaves a stop intersection.
        void ExitStop(GameObject _vehicle){
            
            intersectionTimer.Stop();
            intersectionTimer.Reset();

            _vehicle.GetComponent<VehicleAI>().vehicleStatus = Status.GO;
            vehiclesInIntersection.Remove(_vehicle);
            vehiclesQueue.Remove(_vehicle);

            _vehicle.GetComponent<TruckInfo>().nowStatus = NowStatus.NONE;

            if(vehiclesQueue.Count > 0 && vehiclesInIntersection.Count == 0){
                vehiclesQueue[0].GetComponent<VehicleAI>().vehicleStatus = Status.GO;
                vehiclesQueue[0].GetComponent<TruckInfo>().nowStatus = NowStatus.WAITING;
            }
        }

        // Triggers the red light status for a vehicle when it enters a traffic light intersection.
        void TriggerLight(GameObject _vehicle){
            VehicleAI vehicleAI = _vehicle.GetComponent<VehicleAI>();
            int vehicleSegment = vehicleAI.GetSegmentVehicleIsIn();

            // If the vehicle is in a red light segment, set its status to STOP and add it to the queue.
            if(IsRedLightSegment(vehicleSegment))
            {
                vehicleAI.vehicleStatus = Status.STOP;
                vehiclesQueue.Add(_vehicle);
            }
            // If not in a red light segment, set the vehicle status to GO.
            else
            {
                vehicleAI.vehicleStatus = Status.GO;
            }
        }

        // Exits the traffic light status for a vehicle when it leaves a traffic light intersection.
        void ExitLight(GameObject _vehicle)
        {
            _vehicle.GetComponent<VehicleAI>().vehicleStatus = Status.GO;
        }

        // Checks if a given segment is currently under a red light in the traffic light intersection.
        bool IsRedLightSegment(int _vehicleSegment)
        {
            // Check the current group of red lights and see if the vehicle's segment is included.
            if(currentRedLightsGroup == 1){
                foreach(Segment segment in lightsNbr1){
                    if(segment.id == _vehicleSegment)
                        return true;
                }
            }
            else{
                foreach(Segment segment in lightsNbr2){
                    if(segment.id == _vehicleSegment)
                        return true;
                }
            }
            return false;
        }

        // Moves vehicles in the queue when the traffic light changes to green for their segment.
        void MoveVehiclesQueue(){
            //Move all vehicles in queue
            List<GameObject> nVehiclesQueue = new List<GameObject>(vehiclesQueue);
            foreach(GameObject vehicle in vehiclesQueue)
            {
                int vehicleSegment = vehicle.GetComponent<VehicleAI>().GetSegmentVehicleIsIn();
                // If the vehicle's segment is not under a red light, set its status to GO and remove it from the queue.
                if(!IsRedLightSegment(vehicleSegment))
                {
                    vehicle.GetComponent<VehicleAI>().vehicleStatus = Status.GO;
                    nVehiclesQueue.Remove(vehicle);
                }
            }
            vehiclesQueue = nVehiclesQueue;
        }

        // Checks if a vehicle's route is a priority segment.
        bool IsPrioritySegment(string vehicleRouteName){
            foreach(Segment s in prioritySegments){
                if(vehicleRouteName == s.name)
                    return true;
            }
            return false;
        }

        // Checks if a vehicle is already in the intersection.
        bool IsAlreadyInIntersection(GameObject _target){
            foreach(GameObject vehicle in vehiclesInIntersection){
                if(vehicle.GetInstanceID() == _target.GetInstanceID()) return true;
            }
            foreach(GameObject vehicle in vehiclesQueue){
                if(vehicle.GetInstanceID() == _target.GetInstanceID()) return true;
            }

            return false;
        } 

        // Stores the current state of the intersection for later resumption.
        private List<GameObject> memVehiclesQueue = new List<GameObject>();
        private List<GameObject> memVehiclesInIntersection = new List<GameObject>();
        
        // Saves the current state of the intersection queue and vehicles in the intersection.
        public void SaveIntersectionStatus(){
            memVehiclesQueue = vehiclesQueue;
            memVehiclesInIntersection = vehiclesInIntersection;
        }

        // Resumes the intersection state to the saved state.
        public void ResumeIntersectionStatus(){
            foreach(GameObject v in vehiclesInIntersection){
                foreach(GameObject v2 in memVehiclesInIntersection){
                    if(v.GetInstanceID() == v2.GetInstanceID()){
                        v.GetComponent<VehicleAI>().vehicleStatus = v2.GetComponent<VehicleAI>().vehicleStatus;
                        break;
                    }
                }
            }
            foreach(GameObject v in vehiclesQueue){
                foreach(GameObject v2 in memVehiclesQueue){
                    if(v.GetInstanceID() == v2.GetInstanceID()){
                        v.GetComponent<VehicleAI>().vehicleStatus = v2.GetComponent<VehicleAI>().vehicleStatus;
                        break;
                    }
                }
            }
        }
    }
}
