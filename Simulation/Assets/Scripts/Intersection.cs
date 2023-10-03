using System.Collections.Generic;
using System.Diagnostics;
using UnityEngine;

namespace TrafficSimulation{
    public enum IntersectionType{
        STOP,
        TRAFFIC_LIGHT
    }

    public class Intersection : MonoBehaviour
    {   
        public IntersectionType intersectionType;
        public int id;  

        //For stop only
        public List<Segment> prioritySegments;

        //For traffic lights only
        public float lightsDuration = 8;
        public float orangeLightDuration = 2;
        public List<Segment> lightsNbr1;
        public List<Segment> lightsNbr2;

        private List<GameObject> vehiclesQueue;
        private List<GameObject> vehiclesInIntersection;

        private TrafficSystem trafficSystem;
        
        [HideInInspector] public int currentRedLightsGroup = 1;

        private Target currentTarget;

        // Time to slow down to zero speed
        public float slowingTime = 1f; 
        private float invokeTime = 5f;

        private Stopwatch intersectionTimer;
        private float intersectionTimeLimit = 30f;
        
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

        void SwitchLights(){

            if(currentRedLightsGroup == 1) currentRedLightsGroup = 2;
            else if(currentRedLightsGroup == 2) currentRedLightsGroup = 1;            
            
            //Wait few seconds after light transition before making the other car move (= orange light)
            Invoke("MoveVehiclesQueue", orangeLightDuration);
        }

        void OnTriggerEnter(Collider _other) {
            //Check if vehicle is already in the list if yes abort
            //Also abort if we just started the scene (if vehicles inside colliders at start)
            if(IsAlreadyInIntersection(_other.gameObject) || Time.timeSinceLevelLoad < .5f) return;

            if(_other.tag == "AutonomousVehicle" && intersectionType == IntersectionType.STOP)
            {
                TriggerStop(_other.gameObject);
            }
        }

        void OnTriggerExit(Collider _other) {
            if(_other.tag == "AutonomousVehicle" && intersectionType == IntersectionType.STOP)
                ExitStop(_other.gameObject);
            else if(_other.tag == "AutonomousVehicle" && intersectionType == IntersectionType.TRAFFIC_LIGHT)
                ExitLight(_other.gameObject);
        }

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

        void TriggerLight(GameObject _vehicle){
            VehicleAI vehicleAI = _vehicle.GetComponent<VehicleAI>();
            int vehicleSegment = vehicleAI.GetSegmentVehicleIsIn();

            if(IsRedLightSegment(vehicleSegment)){
                vehicleAI.vehicleStatus = Status.STOP;
                vehiclesQueue.Add(_vehicle);
            }
            else{
                vehicleAI.vehicleStatus = Status.GO;
            }
        }

        void ExitLight(GameObject _vehicle){
            _vehicle.GetComponent<VehicleAI>().vehicleStatus = Status.GO;
        }

        bool IsRedLightSegment(int _vehicleSegment){
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

        void MoveVehiclesQueue(){
            //Move all vehicles in queue
            List<GameObject> nVehiclesQueue = new List<GameObject>(vehiclesQueue);
            foreach(GameObject vehicle in vehiclesQueue){
                int vehicleSegment = vehicle.GetComponent<VehicleAI>().GetSegmentVehicleIsIn();
                if(!IsRedLightSegment(vehicleSegment)){
                    vehicle.GetComponent<VehicleAI>().vehicleStatus = Status.GO;
                    nVehiclesQueue.Remove(vehicle);
                }
            }
            vehiclesQueue = nVehiclesQueue;
        }

        bool IsPrioritySegment(string vehicleRouteName){
            foreach(Segment s in prioritySegments){
                if(vehicleRouteName == s.name)
                    return true;
            }
            return false;
        }

        bool IsAlreadyInIntersection(GameObject _target){
            foreach(GameObject vehicle in vehiclesInIntersection){
                if(vehicle.GetInstanceID() == _target.GetInstanceID()) return true;
            }
            foreach(GameObject vehicle in vehiclesQueue){
                if(vehicle.GetInstanceID() == _target.GetInstanceID()) return true;
            }

            return false;
        } 


        private List<GameObject> memVehiclesQueue = new List<GameObject>();
        private List<GameObject> memVehiclesInIntersection = new List<GameObject>();

        public void SaveIntersectionStatus(){
            memVehiclesQueue = vehiclesQueue;
            memVehiclesInIntersection = vehiclesInIntersection;
        }

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
