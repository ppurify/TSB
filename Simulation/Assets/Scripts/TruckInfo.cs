using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using UnityEngine;
using UnityEditor;
using System.IO;

namespace TrafficSimulation{

    public enum NowStatus
    {
        WAITING,
        PROCESSING,
        NONE
    }

    public class TruckInfo : MonoBehaviour
    {

        public List<Vector3> truckWorkStations;
        public int truckWorkStationsNum;
        public Vector3 truckOrigin;
        public Vector3 truckDestination;
        public string truckRouteName;
        public int truckStatus;

        
        private GameObject vehicle;
        private VehicleAI thisVehicleAI;

        private float short_slowingTime = 1f;

        private float long_slowingTime = 5f;

        private float processTime;


        private Vector3 originalPos;

        // 1. tile 75        
        // private float toStationNum = 25f;
        // 2. tile 25
        private float toStationNum = 20f;

        private float checkRange_1 = 5f;
 
        private float checkRange_2 = 13f;

        public List<Vector3> turnStations;


        private GameObject nowStation;
        private Vector3 nowStationPos;
        private CranesInfo nowStationInfo;
        private int nowStation_FinishedVehicle_toLeft;
        private int nowStation_FinishedVehicle_toRight;

        // To check Station's Status
        private float checkDelay = 1f; 

        private SaveFile saveFile;
        private Stopwatch truckTotalWatch;
        private Stopwatch truckStationWatch;
        private Stopwatch noReasonStopWatch;
        [SerializeField]private List<float> truckStationWatchList = new List<float>();

        private ExitPlayMode exitPlayMode;
        private Vector3 startPos;
        private Vector3 firstStationPos;

        private Rigidbody rb;

        public NowStatus nowStatus;
        
        // 한대씩 돌릴 때 필요한 Data
        // private static CreateTruckAndStation createTruckAndStation;
        private static List<CreateTruckData> truckDataList;
        private static bool _isOneByOne = CreateTruckAndStation.isOneByOne;

        private WholeProcess wholeProcess;

        // Start is called before the first frame update
        void Awake()
        {   
            vehicle = this.gameObject;
            thisVehicleAI = vehicle.GetComponent<VehicleAI>();

            truckTotalWatch = new Stopwatch();
            truckStationWatch = new Stopwatch();
            noReasonStopWatch = new Stopwatch();
            // createTruckAndStation = GameObject.Find("Roads").GetComponent<CreateTruckAndStation>();
        }

        void Start()
        {
            truckStatus = 0;

            truckTotalWatch.Start();
            truckStationWatch.Start();

            exitPlayMode = GameObject.Find("Roads").GetComponent<ExitPlayMode>();
            rb = vehicle.GetComponent<Rigidbody>();

            nowStatus = NowStatus.NONE;

            saveFile = GameObject.Find("Roads").GetComponent<SaveFile>();
            wholeProcess = GameObject.Find("Roads").GetComponent<WholeProcess>();
        }
        
        void Update()
        {
            if((thisVehicleAI.vehicleStatus == Status.GO || thisVehicleAI.vehicleStatus == Status.SLOW_DOWN) && rb.velocity.magnitude < 0.05f && nowStatus == NowStatus.NONE)
            {  
                Vector3 nowPos = vehicle.transform.position;

                float vehicleRotationY = vehicle.transform.rotation.eulerAngles.y;

                // 0도
                float bias = 45f;
                float move = 0.05f;
                if((vehicleRotationY >= 0 - bias && vehicleRotationY <= 0 + bias)|| (vehicleRotationY >= 360 - bias && vehicleRotationY <= 360 + bias))
                {
                    vehicle.transform.position = nowPos + new Vector3(0f, 0f, move);
                    // UnityEngine.Debug.Log(vehicle.name + " Move up side");
                    if(thisVehicleAI.vehicleStatus == Status.GO)
                    {
                        vehicle.transform.rotation = Quaternion.Euler(0f, 0f, 0f);
                    }
                }

                // 180도
                else if((vehicleRotationY >= 180 - bias && vehicleRotationY <= 180 + bias) || (vehicleRotationY >= -180 - bias && vehicleRotationY <= -180 + bias))
                {
                    vehicle.transform.position = nowPos + new Vector3(0f, 0f, -move);
                    // UnityEngine.Debug.Log(vehicle.name + " Move down side");
                    if(thisVehicleAI.vehicleStatus == Status.GO)
                    {
                        vehicle.transform.rotation = Quaternion.Euler(0f, 180f, 0f);
                    }
                }

                // 90도 _rotationY >= 85 && _rotationY <= 95
                else if((vehicleRotationY >= 90 - bias && vehicleRotationY <= 90 + bias) || (vehicleRotationY >= -270 - bias && vehicleRotationY <= -270 + bias))
                {
                    vehicle.transform.position = nowPos + new Vector3(move, 0f, 0f);
                    // UnityEngine.Debug.Log(vehicle.name + " Move right side");
                    if(thisVehicleAI.vehicleStatus == Status.GO)
                    {
                        vehicle.transform.rotation = Quaternion.Euler(0f, 90f, 0f);
                    }
                }

                // 270도
                else if((vehicleRotationY >= -90 - bias && vehicleRotationY <= -90 + bias) || (vehicleRotationY >= 270 - bias && vehicleRotationY <= 270 + bias))
                {
                    vehicle.transform.position = nowPos + new Vector3(-move, 0f, 0f);
                    // UnityEngine.Debug.Log(vehicle.name + " Move left side");
                    if(thisVehicleAI.vehicleStatus == Status.GO)
                    {
                        vehicle.transform.rotation = Quaternion.Euler(0f, -90f, 0f);
                    }
                }

                else
                {
                    UnityEngine.Debug.LogError("You have to again check vehicle's rotationY");
                }

            }
        }
        
        void OnTriggerEnter(Collider _other)
        {   
            if(_other.gameObject.tag == "Station")
            {
                // Get Station's Information
                nowStation = _other.gameObject;
                nowStationPos = nowStation.transform.position;
                nowStationInfo = nowStation.GetComponent<CranesInfo>();

                nowStation_FinishedVehicle_toLeft = nowStationInfo.finishedQueueList_toLeft.Count;
                nowStation_FinishedVehicle_toRight = nowStationInfo.finishedQueueList_toRight.Count;

                if(vehicle == null)
                {
                    vehicle = this.gameObject;
                    thisVehicleAI = vehicle.GetComponent<VehicleAI>();
                }

                if(truckStatus == 0)
                {
                    startPos = GameObject.Find(truckRouteName).transform.GetChild(0).transform.position;
                    firstStationPos = truckWorkStations[0];
                }

                // 방금 전에 작업 완료한 트럭인 경우에는 안멈추도록
                if(truckStatus == 0 | (truckStatus != 0 && truckWorkStations[truckStatus -1] != nowStationPos))
                {
                    if(CheckRotation_IsToRight(vehicle))
                    {   
                        if(nowStation_FinishedVehicle_toRight > 0)
                        {   
                            // 작업이 완료된 트럭이 있다면 도착한 vehicle 감속 및 멈춤
                            StartCoroutine(ReduceSpeed(vehicle, short_slowingTime));
                            thisVehicleAI.vehicleStatus = Status.STOP;
                            nowStatus = NowStatus.WAITING;

                            StartCoroutine(CheckFinishedQueue(checkDelay, nowStation_FinishedVehicle_toRight));
                            
                        }
                    }

                    // 왼쪽 방향으로 가는 경우
                    else
                    {   
                        if(nowStation_FinishedVehicle_toLeft > 0)
                        {
                            // 작업이 완료된 트럭이 있다면 도착한 vehicle 감속 및 멈춤

                            StartCoroutine(ReduceSpeed(vehicle, short_slowingTime));
                            thisVehicleAI.vehicleStatus = Status.STOP;
                            nowStatus = NowStatus.WAITING;

                            StartCoroutine(CheckFinishedQueue(checkDelay, nowStation_FinishedVehicle_toLeft));
                        }
                    }
                }

                if(truckStatus < truckWorkStations.Count)
                {
                    // 작업하는 곳인지 확인
                    Vector3 toWorkStationPos= truckWorkStations[truckStatus];
                    // 트럭이 작업해야하는 곳인 경우
                    if(nowStationPos == toWorkStationPos)
                    {   
                        StartCoroutine(WorkingProcess());
                    }
                }
            }

            else if(_other.gameObject.tag == "AutonomousVehicle")
            {
                UnityEngine.Debug.LogError(this.name + " is crashed with " + _other.gameObject.name);
            }

        }
     

         private IEnumerator WorkingProcess()
        {   
            nowStatus = NowStatus.PROCESSING;
            // 시작 위치와 첫번째 작업장이 같은 경우 or 이전의 작업장과 현재 작업장이 같은 경우 
            if(IsStartPosEqualNowStation(startPos, nowStationPos, truckStatus) || truckStatus > 0 && truckWorkStations[truckStatus -1] == truckWorkStations[truckStatus])
            {
                if(rb == null)
                {
                    rb = vehicle.GetComponent<Rigidbody>();
                }

                rb.velocity = Vector3.zero;
            }

            else
            {
                // 감속
                thisVehicleAI.vehicleStatus = Status.SLOW_DOWN;
                yield return StartCoroutine(ReduceSpeed(vehicle, long_slowingTime));   
            }

            
            thisVehicleAI.vehicleStatus = Status.STOP;

            if(truckStationWatch == null)
            {
                UnityEngine.Debug.LogError(this.name + "  stationWatch Component is null !!!");
            }
            
            if(truckStationWatchList == null)
            {
                UnityEngine.Debug.LogError(this.name + " truck Station Watch List is null !!!");
            }

            
            float stationArrivalTime = truckStationWatch.ElapsedMilliseconds / 1000f * Time.timeScale;

            truckStationWatchList.Add(stationArrivalTime);
           
            originalPos = vehicle.transform.position;

            truckStationWatch.Stop();
           
            MoveToProcess();
            truckStationWatch.Reset();
        }
        
        private void MoveToProcess()
        {
            nowStatus = NowStatus.WAITING;

            vehicle.SetActive(false);
        
            vehicle.transform.position = nowStationPos + new Vector3(0, 0, toStationNum);

            nowStation.GetComponent<CranesInfo>().processQueueList.Add(vehicle);

            InvokeRepeating("checkStationStatus", 1f, 1f);
        }

        private void Processing()
        {   
            // UnityEngine.Debug.Log(this.name + " processing ---> station : " + nowStationPos);

            nowStatus = NowStatus.PROCESSING;

            // Get Station information
            nowStation.GetComponent<CranesInfo>().craneStatus += 1;

            nowStation.GetComponent<CranesInfo>().processQueueList.Remove(vehicle);

            nowStation.GetComponent<CranesInfo>().processList.Add(vehicle);

            processTime = nowStationInfo.craneProcessTime;
            Invoke("FinishProcess", processTime);
        }

        private void FinishProcess()
        {
            nowStation.GetComponent<CranesInfo>().craneStatus -= 1;
            nowStation.GetComponent<CranesInfo>().processList.Remove(vehicle);

            PlusFinishedVehicle(nowStationInfo, vehicle);

            truckStatus+= 1;

            InvokeRepeating("CheckRoad", 3f, 3f);
        }

        private void checkStationStatus()
        {
            if(IsStationAvailable(nowStation))
            {
                CancelInvoke("checkStationStatus");

                // destination이 아닌 경우
                if(!IsDestination(nowStationPos, truckWorkStations, truckStatus, truckWorkStationsNum))
                {
                    Processing();
                }
                
                // destination인 경우
                else
                {
                    LastProcessing();
                }
                
            }
        }
        
        private void CheckRoad()
        {   
            // UnityEngine.Debug.Log(originalPos +" CheckRoad ");
            if(!ExistAnyTruck(originalPos, checkRange_1, checkRange_2))
            {
                CancelInvoke("CheckRoad");
                MoveToOriginalPos();
            }

            else
            {
                // UnityEngine.Debug.Log(originalPos + " ExistAnyTruck");
            }
        }

        private void MoveToOriginalPos()
        {   
            // UnityEngine.Debug.Log(vehicle.name + " move from " + nowStationPos + " to Original Pos ---> CheckRotation_IsToRight(vehicle) : " + CheckRotation_IsToRight(vehicle));

            if(CheckRotation_IsToRight(vehicle))
            {   
                originalPos = nowStationPos + new Vector3(0, 0, -7.5f);
            }

            else
            {
                originalPos = nowStationPos + new Vector3(0, 0, 7.5f);
            }

            vehicle.transform.position = originalPos;
        
            vehicle.SetActive(true);

            MinusFinishedVehicle(nowStationInfo, vehicle);

            thisVehicleAI.vehicleStatus = Status.GO;

            truckStationWatch.Start();
            nowStatus = NowStatus.NONE;
        }

        private void LastProcessing()
        {   
            // UnityEngine.Debug.Log(this.name + " Last Processing at " + nowStationPos + " station ");
            // Get Station information
            nowStationInfo.craneStatus += 1;
            nowStationInfo.processQueueList.Remove(vehicle);

            rb.velocity = Vector3.zero;
            thisVehicleAI.vehicleStatus = Status.STOP;

            processTime = nowStationInfo.craneProcessTime;
            Invoke("FinishLastProcess", processTime);
        }

        private void FinishLastProcess()
        {
            truckTotalWatch.Stop();
            // UnityEngine.Debug.Log(vehicle.name + " truckTotalWatch stop ");

            float truckTotalTime = truckTotalWatch.ElapsedMilliseconds / 1000f * Time.timeScale;
            
            // UnityEngine.Debug.Log(vehicle.name + " process done --> truckTotalTime : " + truckTotalTime);

            nowStationInfo.craneStatus -= 1;

            
            if(saveFile == null)
            {
                saveFile = GameObject.Find("Roads").GetComponent<SaveFile>();
            }

           
            if(truckTotalWatch == null)
            {
                UnityEngine.Debug.LogError(this.name + " _truckTimer.totalWatch is null !!!");
            }

            
            if(exitPlayMode == null)
            {
                exitPlayMode = GameObject.Find("Roads").GetComponent<ExitPlayMode>();
            }

            exitPlayMode.nowTruckCount ++;
            truckDestination = nowStationPos;


            ResultsData resultsData = ScriptableObject.CreateInstance<ResultsData>();
            resultsData.CreateResultData(saveFile.filePath, vehicle.name, truckRouteName, truckOrigin, truckDestination, truckTotalTime, truckStationWatchList);
            SaveFile.resultsDataList.Add(resultsData);

            // UnityEngine.Debug.Log(vehicle.name + " saved result data !!! ");
            
            // 한대씩 돌릴 때
            if(_isOneByOne)
            {   
                if(wholeProcess.isPrevExist)
                {
                    truckDataList = CreateTruckAndStation.truckDataList_1;
                }

                else
                {
                    truckDataList = CreateTruckAndStation.truckDataList_2;
                }

                if(exitPlayMode.nowTruckCount < exitPlayMode.totalTruckCount)
                {
                    CreateTruckAndStation.CreateTruckOneByOne(truckDataList[exitPlayMode.nowTruckCount]);
                }
            }

            if(exitPlayMode.nowTruckCount == exitPlayMode.totalTruckCount)
            {  
                WholeProcess.currentFileCount++;

                if(WholeProcess.currentFileCount < WholeProcess.totalFileCount) 
                {
                    if(WholeProcess.folderCount == 2)
                    {
                        string prevRouteFilename = Path.GetFileName(wholeProcess.currentPrevRouteFilePath);
                        string nowRouteFilename = Path.GetFileName(wholeProcess.currentNowRouteFilePath);
                        GameObject prevRouteGO = GameObject.Find(prevRouteFilename);
                        GameObject nowRouteGO = GameObject.Find(nowRouteFilename);
                        
                        Destroy(prevRouteGO);
                        Destroy(nowRouteGO);
                    }

                    else
                    {
                        if(wholeProcess.isPrevExist)
                        {
                            string prevRouteFilename = Path.GetFileName(wholeProcess.currentPrevRouteFilePath);
                            GameObject prevRouteGO = GameObject.Find(prevRouteFilename);
                            Destroy(prevRouteGO);       
                        }

                        else
                        {
                            string nowRouteFilename = Path.GetFileName(wholeProcess.currentNowRouteFilePath);
                            GameObject nowRouteGO = GameObject.Find(nowRouteFilename);
                            Destroy(nowRouteGO);
                        }
                    }

                    wholeProcess.Process();
                }
                
                List<ResultsData> dataList = SaveFile.resultsDataList;
                foreach(ResultsData data in dataList)
                {
                    saveFile.SaveToCSV(data.FilePath, data.Vehicle, data.Route, data.Origin, data.Destination, data.TotalTime, data.StopwathTimeList);
                    UnityEngine.Debug.Log("Save " + data.FilePath + "  --> " + data.Vehicle + " data");
                }
            }

            UnityEngine.Debug.Log(vehicle.name + " is finished !!!");
        
            Destroy(vehicle);
        }
        

        private bool CheckRotation_IsToRight(GameObject _vehicle)
        {
            if (_vehicle == null)
            {
                UnityEngine.Debug.LogError(this.name + " --> The _vehicle object is null. Make sure it is properly initialized before calling this method.");
                return false;
            }

            float _rotationY = _vehicle.transform.eulerAngles.y;

            if(_rotationY >= 85 && _rotationY <= 95)
            {
                return true;
            }

            else
            {
                return false;
            }
        }

        private bool IsStationAvailable(GameObject _station)
        {
            bool isAvailable = false;
            
            // Get Station's Status
            CranesInfo _craneInfo = _station.GetComponent<CranesInfo>();
            int _craneStatus = _craneInfo.craneStatus;
            int _craneCapacity = _craneInfo.craneCapacity;

            if(_craneStatus < _craneCapacity)
            {
                isAvailable = true;
            }

            return isAvailable;
        }


        public IEnumerator ReduceSpeed(GameObject _vehicle, float _slowingTime)
        {   
            Rigidbody rb = _vehicle.GetComponent<Rigidbody>();
            
            Vector3 initialVelocity = rb.velocity;
            float elapsedTime = 0f;

            while (elapsedTime < _slowingTime)
            {
                rb.velocity = Vector3.Lerp(initialVelocity, Vector3.zero, elapsedTime / _slowingTime);
                elapsedTime += Time.deltaTime;
                yield return null;
            }

            rb.velocity = Vector3.zero; // Ensure velocity is set to zero
        }

        private IEnumerator CheckFinishedQueue(float _checkDelay, int _nowStationFinshedQueueCount)
        {
            while(_nowStationFinshedQueueCount > 0)
            {
                yield return new WaitForSeconds(_checkDelay);

                if(CheckRotation_IsToRight(vehicle))
                {
                    _nowStationFinshedQueueCount = nowStation.GetComponent<CranesInfo>().finishedQueueList_toRight.Count;
                }

                else
                {
                    _nowStationFinshedQueueCount = nowStation.GetComponent<CranesInfo>().finishedQueueList_toLeft.Count;
                }
            }

            thisVehicleAI.vehicleStatus = Status.GO;
            nowStatus = NowStatus.NONE;
        }

        private bool ExistAnyTruck(Vector3 _position, float _checkRange_1, float _checkRange_2)
        {
            Collider[] colliders = Physics.OverlapSphere(_position, Mathf.Max(_checkRange_1, _checkRange_2));
            
            foreach (Collider collider in colliders)
            {
                if (collider.CompareTag("AutonomousVehicle"))
                {
                    return true;
                }
            }
            
            return false;
        }


        private void PlusFinishedVehicle(CranesInfo _stationInfo, GameObject _vehicle)
        {   
            if(CheckRotation_IsToRight(vehicle))
            {
                _stationInfo.finishedQueueList_toRight.Add(_vehicle);
            }

            else
            {
                _stationInfo.finishedQueueList_toLeft.Add(_vehicle);
            }
        }


        private void MinusFinishedVehicle(CranesInfo _stationInfo, GameObject _vehicle)
        {   
            if(CheckRotation_IsToRight(_vehicle))
            {
                _stationInfo.finishedQueueList_toRight.Remove(_vehicle);
            }

            else
            {
                _stationInfo.finishedQueueList_toLeft.Remove(_vehicle);
            }
        }


        private bool IsDestination(Vector3 _nowStationPos, List<Vector3> _truckWorkStations, int _truckStatus, int _truckWorkStationsNum)
        {
            return _nowStationPos == _truckWorkStations[_truckWorkStationsNum-1] && _truckStatus == _truckWorkStationsNum - 1;
        }

        private bool IsStartPosEqualNowStation(Vector3 _startPos, Vector3 _nowStaitonPos, int _truckStatus)
        {
            return _startPos == _nowStaitonPos && _truckStatus == 0;
        }

    }
}