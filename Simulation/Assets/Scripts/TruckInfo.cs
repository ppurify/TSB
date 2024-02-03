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
        
        // Truck's Information
        // pickup, drop station's position
        public List<Vector3> truckWorkStations;
        // the number of stations of pickup, drop
        public int truckWorkStationsNum;
        // position of truck's origin
        public Vector3 truckOrigin;
        // position of truck's destination
        public Vector3 truckDestination;
        // the length of truck's path
        public float truckPathLength;
        // completion time of truck without other trucks
        public float truckCompletionTime_alone;
        // Route name of truck
        public string truckRouteName;
        // the status of truck
        public int truckStatus;

        // Entity of truck
        private GameObject vehicle;
        // Vehicle system of truck
        private VehicleAI thisVehicleAI;

        // time to stop
        private float short_slowingTime = 1f;
        private float long_slowingTime = 5f;

        // time to process
        private float processTime;

        // position of truck to record
        private Vector3 originalPos;

        //  move to station's position
        // 1. tile 75        
        // private float toStationNum = 25f;
        // 2. tile 25
        private float toStationNum = 20f;

        // check range to find any truck
        private float checkRange_1 = 5f;
        private float checkRange_2 = 13f;

        // turn station's position of truck
        public List<Vector3> turnStations;

        // Entity of now work station
        private GameObject nowStation;
        // position of now work station
        private Vector3 nowStationPos;
        // Information of now work station
        private CranesInfo nowStationInfo;

        // the number of finished vehicle to move to left side or right side
        private int nowStation_FinishedVehicle_toLeft;
        private int nowStation_FinishedVehicle_toRight;

        // To check Station's Status
        private float checkDelay = 1f; 

        //  save result data
        private SaveFile saveFile;
        
        // stopwatch to record truck's total time
        private Stopwatch truckTotalWatch;
        
        // stopwatch to record truck's travel time
        private Stopwatch truckStationWatch;
        
        // stopwatch to record time if you stop for no reason
        private Stopwatch noReasonStopWatch;

        // list to record truck's travel time
        [SerializeField]private List<float> truckStationWatchList = new List<float>();

        // to exit play mode
        private ExitPlayMode exitPlayMode;
        
        // check start position
        private Vector3 startPos;

        // check first station's position
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
        
        // 아무이유 없이 멈췄을 때 시간 체크 후 움직이도록 살짝 이동해주기
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

            float nowTruckTotalTime = truckTotalWatch.ElapsedMilliseconds / 1000f * Time.timeScale;
            
            if(nowTruckTotalTime >= wholeProcess.limitTotalTime)
            {
                WholeProcess.playAgain = true;
            }
        }
        
        // 차량이 작업 장소에 도착했을 때
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
        }

        // 작업 처리를 위한 함수 
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
        
        // 작업 장소로 이동
        private void MoveToProcess()
        {
            nowStatus = NowStatus.WAITING;

            vehicle.SetActive(false);
        
            vehicle.transform.position = nowStationPos + new Vector3(0, 0, toStationNum);

            nowStation.GetComponent<CranesInfo>().processQueueList.Add(vehicle);

            InvokeRepeating("checkStationStatus", 1f, 1f);
        }

        // 작업 처리
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

        // 작업 처리 완료
        private void FinishProcess()
        {
            nowStation.GetComponent<CranesInfo>().craneStatus -= 1;
            nowStation.GetComponent<CranesInfo>().processList.Remove(vehicle);

            PlusFinishedVehicle(nowStationInfo, vehicle);

            truckStatus+= 1;

            InvokeRepeating("CheckRoad", 3f, 3f);
        }

        // 현재 작업장의 상태를 확인
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
        
        // 작업이 끝난 후 원래 위치로 이동하기 위해 도로 상황을 확인
        private void CheckRoad()
        {   
            // UnityEngine.Debug.Log(originalPos +" CheckRoad ");
            if(!ExistAnyTruck(originalPos, checkRange_1, checkRange_2))
            {
                CancelInvoke("CheckRoad");
                MoveToOriginalPos();
            }
        }

        // 원래 위치로 이동
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

        // 마지막 작업 처리
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

        // 마지막 작업 처리 완료 시 결과 저장
        private void FinishLastProcess()
        {
            truckTotalWatch.Stop();

            float truckCompletionTime = truckTotalWatch.ElapsedMilliseconds / 1000f * Time.timeScale;

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
            resultsData.CreateResultData(saveFile.filePath, vehicle.name, truckRouteName, truckOrigin, truckDestination, truckPathLength, truckCompletionTime_alone, truckCompletionTime, truckStationWatchList);
            SaveFile.resultsDataList.Add(resultsData);

            // UnityEngine.Debug.Log(vehicle.name + " saved result data !!! ");
            
            // 한대씩 돌릴 때
            if(_isOneByOne)
            {   
                if(wholeProcess.isPrevFolder)
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
                wholeProcess.currentFileCount++;

                if(wholeProcess.subFolderCount == 2)
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
                    if(wholeProcess.isPrevFolder)
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
                
                if(wholeProcess.currentFileCount == wholeProcess.totalFileCount)
                {
                    wholeProcess.currentFolderCount ++;
                    wholeProcess.currentFileCount = 0;
                }

                if(wholeProcess.folderCount != wholeProcess.currentFolderCount)
                {
                    wholeProcess.Process();
                }

                if(SaveFile.resultsDataList != null)
                {   
                    saveFile.SaveToCSV();
                }

                else
                {
                    UnityEngine.Debug.LogError("SaveFile.resultsDataList is null !!!");
                }
                
            }
            
            Destroy(vehicle);
        }
        
        // 차량의 회전 방향을 확인 (오른쪽으로 가는지 확인)
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

        // 작업장이 사용 가능한지 확인
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

        // 작업장에 도착하기 전에 감속
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

        // 작업장에 작업이 완료된 차량이 있는지 확인
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

        // 특정 좌표를 기준으로 해당 범위 내에 차량이 존재하는지 확인
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

        // 작업을 완료했을 때, 완료 리스트에 차량 추가
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

        // 차량이 작업 완료 후 작업장을 빠져나간 경우 완료 리스트에서 차량 제거 
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

        // 차량이 작업장에 도착했을 때, 목적지인지 확인
        private bool IsDestination(Vector3 _nowStationPos, List<Vector3> _truckWorkStations, int _truckStatus, int _truckWorkStationsNum)
        {
            return _nowStationPos == _truckWorkStations[_truckWorkStationsNum-1] && _truckStatus == _truckWorkStationsNum - 1;
        }

        // 출발지와 현재 작업장이 같은지 확인
        private bool IsStartPosEqualNowStation(Vector3 _startPos, Vector3 _nowStaitonPos, int _truckStatus)
        {
            return _startPos == _nowStaitonPos && _truckStatus == 0;
        }

    }
}