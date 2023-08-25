using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using System.Text.RegularExpressions;
using System;

namespace TrafficSimulation{
    public class CreateTruckAndStation : MonoBehaviour
    {
        private static string folderPath_1 = "C:\\Users\\USER\\workspace\\TSB\\Traffic_Simulation\\Assets\\Data\\prev\\Trucks\\";
        private static string folderPath_2 = "C:\\Users\\USER\\workspace\\TSB\\Traffic_Simulation\\Assets\\Data\\Variance\\LP_50_40_10\\Trucks\\";
        
        public static string truckFileName_1 = "prev_Truck_70_shortest.csv";
        public static string truckFileName_2 = "now_Truck_1_LP_50_40_10_with_70_shortest.csv";
        private static string truckFilePath_1 = Path.Combine(folderPath_1, truckFileName_1);
        private static string truckFilePath_2 = Path.Combine(folderPath_2, truckFileName_2);

        public static List<CreateTruckData> truckDataList_1 = new List<CreateTruckData>();
        public static List<CreateTruckData> truckDataList_2 = new List<CreateTruckData>();

        private static float truckRotation_y;

        // Station Parameters
        private static Vector3 stationSize = new Vector3(75,10,30);

        private static float stationPos_y = stationSize.y/2;
        private string stationTagName = "Station";

        // 동일한 시작 위치를 가진 트럭들을 포함하는 딕셔너리
        private static Dictionary<Vector3, List<Tuple<string, string, List<Vector3>>>> startPositionDict_1;
        private static Dictionary<Vector3, List<Tuple<string, string, List<Vector3>>>> startPositionDict_2;


        // 동일한 시작 위치를 가진 트럭들의 생성 주기
        private float createDelay = 160f;
        
        // 이전에 스케줄링이 된게 없고 현재 한대만 돌릴 때는 truckIndexPlus_1을 100으로 해주기
        // 두대 돌리거나 이전에 스케줄링 된 걸 돌릴때는 truckIndexPlus_1을 0으로 해주기
        private int truckIndexPlus_1 = 0;
        private int truckIndexPlus_2 = 100;

        private float checkRange_1 = 7f;
        private float checkRange_2 = 3f;
        private float checkDelay = 0.5f;
        
        // file 2개일 때
        public static bool isTwoFile = true;
        // file 1개 일 때
        public static bool isOneFile = false;
        // 1대씩 돌릴 때
        public static bool isOneByOne = false;

        // // 2개 파일일때
        void Start()
        {
            if(truckFilePath_1 != null)
            {
                ReadFile(truckFilePath_1, truckIndexPlus_1);
                CreateStations(truckDataList_1, stationTagName);
            }

            else
            {
                Debug.LogError("check truckFilePath_1.");
            }
            
            if(isTwoFile)
            {
                ReadFile(truckFilePath_2, truckIndexPlus_2);
                CreateStations(truckDataList_2, stationTagName);

                if(ExistRoute(truckDataList_1))
                {   
                    IsDuplicateStartPosition(truckDataList_1, truckIndexPlus_1);
                    CreateTrucks(startPositionDict_1, checkRange_1, checkRange_2, checkDelay);
                }
                
                StartCoroutine(CreateNewTrucksDelay(createDelay));
            }
            
            else if(isOneFile)
            {
                if(ExistRoute(truckDataList_1))
                {   
                    IsDuplicateStartPosition(truckDataList_1, truckIndexPlus_1);
                    CreateTrucks(startPositionDict_1, checkRange_1, checkRange_2, checkDelay);
                }
            }
            
            else if(isOneByOne)
            {   
                if(truckDataList_1 != null)
                {
                    CreateOneTruck_1(truckDataList_1[0]);
                }

                else
                {
                    Debug.LogError("truckDataList_1 is null.");
                }
            }    
        }

        // 경로 유무 확인 함수
        public static void ReadFile(string filePath, int _truckIndexPlus)
        {
            if (!File.Exists(filePath))
            {
                Debug.LogError("File does not exist: " + filePath);
                return;
            }
            
            using (StreamReader reader = new StreamReader(filePath))
            {
                string line;
                bool isFirstLine = true;

                while ((line = reader.ReadLine()) != null)
                {
                    if (isFirstLine)
                    {
                        isFirstLine = false;
                        continue; // Skip the first line
                    }

                    string[] values = line.Split(',');

                    int newTruckNum = int.Parse(values[0]) + _truckIndexPlus;
                    string truckName = "Truck-" + newTruckNum.ToString();
                    
                    int newRouteNum = int.Parse(values[1]) + _truckIndexPlus;
                    string truckRoute = newRouteNum.ToString();


                    CreateTruckData truckData = ScriptableObject.CreateInstance<CreateTruckData>();
                    
                    List<Vector3> workStations = new List<Vector3>();

                    for(int i=2; i<values.Length; i+=3)
                    {   
                        if (values[i] != "" && values[i + 1] != "" && values[i + 2] != "")
                        {
                            string xStr = Regex.Match(values[i], @"\(\s*(-?\d+(\.\d+)?)").Groups[1].Value;
                            string yStr = values[i + 1];
                            string zStr = Regex.Match(values[i + 2], @"(-?\d+(\.\d+)?)\s*\)").Groups[1].Value;

                            float x = float.Parse(xStr);
                            float y = float.Parse(yStr);
                            float z = float.Parse(zStr);

                            Vector3 station = new Vector3(x, y, z);

                            workStations.Add(station);
                        }
                        
                        else
                        {
                            break; // No more values in the next column, exit the loop
                        }
                    }

                    truckData.CreateData(truckName, truckRoute, workStations);

                    if(!isTwoFile | _truckIndexPlus == 0)
                    {
                        truckDataList_1.Add(truckData);
                    }

                    else
                    {
                        truckDataList_2.Add(truckData);
                    }
                }
            }

        }

        public static bool ExistRoute(List<CreateTruckData> dataList)
        {
            // Print the truck data
            foreach(CreateTruckData data in dataList)
            {
                if(!GameObject.Find("Route-"+ data.Route))
                {
                    Debug.LogError("Route does not exist: " + data.Route);
                    return false;
                }
            }

            return true;
        }

       
        // 트럭 시작 위치에 따른 회전 방향 설정 함수
        public static float GetTruckRotation(Transform routeTransform, string routeName)
        {
            Vector3 position_1 = routeTransform.Find(routeName + "/Waypoint-0").transform.position;
            Vector3 position_2 = routeTransform.Find(routeName + "/Waypoint-1").transform.position;
            
            if(position_1.x == position_2.x)
            {   
                // If the truck is moving in the positive z direction
                if(position_1.z - position_2.z < 0)
                {
                    truckRotation_y = 0;
                }

                // If the truck is moving in the negative z direction
                else
                {
                    truckRotation_y = 180;
                }
            }

            else if(position_1.z == position_2.z)
            {
                // If the truck is moving in the positive x direction
                if(position_1.x - position_2.x < 0)
                {
                    truckRotation_y = 90;
                }

                // If the truck is moving in the negative x direction
                else
                {
                    truckRotation_y = 270;
                }
            }

            // Debug.Log(routeName + " --> Truck Rotation: " + truckRotation_y);
            return truckRotation_y;
        }


        // Station 생성 함수
        public void CreateStations(List<CreateTruckData> dataList, string _stationTagName)
        {   
            GameObject stationsOB = GameObject.Find("Stations");

            if(stationsOB == null)
            {
                // Create empty game object named "Stations"
                stationsOB = new GameObject("Stations");
                stationsOB.transform.position = Vector3.zero;
            }

            foreach(CreateTruckData data in dataList)
            {
                if(data.WorkStations.Count > 0)
                {   
                    for(int i = 0; i <data.WorkStations.Count; i++)
                    {
                        Vector3 workStation = data.WorkStations[i];

                        string workStationName = workStation.ToString();

                        // Create a station
                        if(!ExistStation(stationsOB.name, workStationName))
                        {
                            GameObject workStationOB = new GameObject(workStationName);
                            workStationOB.transform.parent = stationsOB.transform;
                            workStationOB.transform.position = workStation;
                            if(ExistTag(_stationTagName))
                            {
                                workStationOB.tag = _stationTagName;
                            }

                            else
                            {
                                Debug.LogError("Tag does not exist: " + _stationTagName);
                            }
                            
                            workStationOB.AddComponent<CranesInfo>();
                            AddCollider(workStationOB);
                        }
                    }
                }
                
                else
                {
                    Debug.LogError("No stations found for truck: " + data.Name);
                }

            }
        }


        // Station 유무 확인 함수
        public static bool ExistStation(string parentOBName, string stationName)
        {   
            bool isExist = true;
            if(GameObject.Find(parentOBName + "/" + stationName) == null)
            {
                isExist = false;
            }

            return isExist;
        }

        
        // 콜라이더 추가 함수
        public static void AddCollider(GameObject obj)
        {
            BoxCollider bc = obj.AddComponent<BoxCollider>();
            bc.size = stationSize;
            Vector3 center = bc.center;
            center.y = stationPos_y;
            bc.center = center;
            bc.isTrigger = true;
        }
        
        
        // 딕셔너리 생성 함수
        private static void IsDuplicateStartPosition(List<CreateTruckData> dataList, float _truckIndexPlus)
        {
            Debug.Log("dataList.Count: " + dataList.Count + " , _truckIndexPlus: " + _truckIndexPlus);

            if(isOneFile | _truckIndexPlus == 0)
            {
                startPositionDict_1 = new Dictionary<Vector3, List<Tuple<string, string, List<Vector3>>>>();
            }

            else
            {
                startPositionDict_2 = new Dictionary<Vector3, List<Tuple<string, string, List<Vector3>>>>();
            }

            foreach(CreateTruckData data in dataList)
            {   
                string parentName = "Route-" + data.Route;
                string childName = parentName + "/Waypoint-0";
                
                GameObject parentOB = GameObject.Find(parentName);

                if(parentOB != null)
                {
                    Transform childTransform = parentOB.transform.Find(childName);

                    if(childTransform != null)
                    {
                        Vector3 startPoint = childTransform.position;

                        Tuple<string, string, List<Vector3>> _truckData = Tuple.Create(data.Name, parentName, data.WorkStations);

                        if(isOneFile | _truckIndexPlus == 0)
                        {
                            if(startPositionDict_1.ContainsKey(startPoint))
                            {  
                                startPositionDict_1[startPoint].Add(_truckData);
                            }

                            else
                            {
                                startPositionDict_1[startPoint] = new List<Tuple<string, string, List<Vector3>>> { _truckData };
                            }
                        }

                        else
                        {
                            if(startPositionDict_2.ContainsKey(startPoint))
                            {  
                                startPositionDict_2[startPoint].Add(_truckData);
                            }

                            else
                            {
                                startPositionDict_2[startPoint] = new List<Tuple<string, string, List<Vector3>>> { _truckData };
                            }
                        }
                        
                    }

                    else
                    {
                        Debug.LogError("Child object not found: " + childName);
                    }
                }

                else
                {
                    Debug.LogError("Parent object not found: " + parentName);
                }
            }
        }

        
        // 출발 위치가 동일한 트럭이 있는지 확인한 후 트럭 생성하는 함수
        private void CreateTrucks(Dictionary<Vector3, List<Tuple<string, string, List<Vector3>>>> _dictionary, float _checkRange_1, float _checkRange_2, float _checkDelay)
        {   
            if(_dictionary == null)
            {
                Debug.LogError("Dictionary is null.");
            }

            // Print the duplicate start positions
            foreach (KeyValuePair<Vector3, List<Tuple<string, string, List<Vector3>>>> kvp in _dictionary)
            {   
                // Debug.Log("kvp.Value.Count: " + kvp.Value.Count);

                Vector3 key = kvp.Key;
                List<Tuple<string, string, List<Vector3>>> values = kvp.Value;

                // 출발 위치가 동일한 트럭이 있는 경우
                if(values.Count > 1)
                {   
                    StartCoroutine(DuplicatePositionCreateTruck(values));
                }

                // 출발 위치가 동일한 트럭이 없는 경우
                else
                {   
                    StartCoroutine(CreateOneTruck(values[0], _checkRange_1, _checkRange_2, _checkDelay));
                }
            }
        }
        

        // 트럭 생성 함수
        public void CreateTruck(string _truckName, string _routeName, List<Vector3> _workStaions)
        {
            // Generate a random number between 1 and 4 (inclusive)
            // int randomNumber = UnityEngine.Random.Range(1, 5);
            // string truckPrefabName = "Truck" + randomNumber.ToString();
            string truckPrefabName = "Truck7";
   
            GameObject truckPrefab = Resources.Load(truckPrefabName) as GameObject;

            if (truckPrefab != null)
            {
                GameObject truck = Instantiate(truckPrefab);
                truck.name = _truckName;
                Transform routeTransform = GameObject.Find(_routeName).transform;

                Vector3 routePosition = routeTransform.Find(_routeName + "/Waypoint-0").transform.position;
                truck.transform.position = new Vector3(routePosition.x, 0f, routePosition.z);
                truck.transform.rotation = Quaternion.Euler(0, GetTruckRotation(routeTransform, _routeName), 0);

                // Set the truck's route
                truck.GetComponent<VehicleAI>().trafficSystem = GameObject.Find(_routeName).GetComponent<TrafficSystem>();

                // Set the truck's work stations and destination
                if(truck.GetComponent<TruckInfo>() == null)
                {   
                    truck.AddComponent<TruckInfo>();
                }

                TruckInfo truckInfo = truck.GetComponent<TruckInfo>();
                truckInfo.truckWorkStations = _workStaions;
                truckInfo.truckWorkStationsNum = _workStaions.Count;

                int workStationCount = _workStaions.Count;
                // truckInfo.truckOrigin = _workStaions[0];
                truckInfo.truckOrigin = truck.transform.position;
                // truckInfo.truckDestination = _workStaions[workStationCount - 1];
                truckInfo.truckRouteName = _routeName;
                truckInfo.turnStations = GameObject.Find(_routeName).GetComponent<RouteInfo>().uTurnStations;
            }

            else
            {
                Debug.LogError("Truck prefab not found: " + truckPrefabName);
            }
        }

        
        // 출발 위치가 동일한 트럭이 있는 경우 트럭 생성 함수
        private IEnumerator DuplicatePositionCreateTruck(List<Tuple<string, string, List<Vector3>>> _values)
        {
            int duplivatedTruckCount = 0;

            foreach (Tuple<string, string, List<Vector3>> value in _values)
            {   
                string truckName = value.Item1;
                string routeName = value.Item2;
                
                List<Vector3> truckWorkStations = value.Item3;
                CreateTruck(truckName, routeName, truckWorkStations);
                // Debug.Log(truckName + " has duplicated position.");
                if(duplivatedTruckCount > 0)
                {
                    GameObject waitedTruck = GameObject.Find(truckName);

                    if(waitedTruck != null)
                    {
                        waitedTruck.GetComponent<BoxCollider>().enabled = false;
                        waitedTruck.GetComponent<VehicleAI>().vehicleStatus = Status.STOP;
                        
                        yield return new WaitForSeconds(0.5f);

                        while(ExistAnyTruck(waitedTruck.transform.position, 6f, 3f))
                        {
                            yield return new WaitForSeconds(0.1f);
                        }

                        waitedTruck.GetComponent<BoxCollider>().enabled = true;
            
                        waitedTruck.GetComponent<VehicleAI>().vehicleStatus = Status.GO;
                    }

                    else
                    {
                        Debug.LogError("Waited truck not found: " + truckName);
                    }
                }
                duplivatedTruckCount++;
            }
        }

        
        // Tag 존재하는지 확인하는 함수
        private bool ExistTag(string _tagName)
        {
            foreach(string existingTag in UnityEditorInternal.InternalEditorUtility.tags)
            {
                if(existingTag == _tagName)
                {
                    return true;
                }
            }
            return false;
        }

        private bool ExistAnyTruck(Vector3 _position, float _checkRange_1, float _checkRange_2)
        {
            Collider[] colliders = Physics.OverlapSphere(_position, Mathf.Max(_checkRange_1, _checkRange_2));
            
            foreach (Collider collider in colliders)
            {
                if (collider.CompareTag("AutonomousVehicle"))
                {
                    // UnityEngine.Debug.Log("Truck detected: " + collider.gameObject.name);
                    return true;
                }
            }
            
            return false;
        }
    
        private IEnumerator CreateNewTrucksDelay(float _createDelay)
        {
            yield return new WaitForSeconds(_createDelay);

            // Create new trucks

            // ReadFile(truckFilePath_2, truckIndexPlus_2);
            // CreateStations(truckDataList_2, stationTagName);

            if(ExistRoute(truckDataList_2))
            {   
                IsDuplicateStartPosition(truckDataList_2, truckIndexPlus_2);
                CreateTrucks(startPositionDict_2, checkRange_1, checkRange_2, checkDelay);
            }

            else
            {
                Debug.LogError("truckDataList_2's Route doesn't found.");
            }
        }


        private IEnumerator CreateOneTruck(Tuple<string, string, List<Vector3>> _value, float _checkRange_1, float _checkRange_2, float _checkDelay)
        {
            string _truckName = _value.Item1;
            string _routeName = _value.Item2;
            List<Vector3> _truckWorkStations =_value.Item3;

            Transform _routeTransform = GameObject.Find(_routeName).transform;
            Vector3 _routePosition = _routeTransform.Find(_routeName + "/Waypoint-0").transform.position;
            Vector3 _position = new Vector3(_routePosition.x, 0f, _routePosition.z);

            while(ExistAnyTruck(_position, _checkRange_1, _checkRange_2))
            {
                yield return new WaitForSeconds(_checkDelay);
            }

            CreateTruck(_truckName, _routeName, _truckWorkStations);
        }
            

        public void CreateOneTruck_1(CreateTruckData _value)
        {   
            string _truckName = _value.Name;
            string _routeName = "Route-" + _value.Route;
            List<Vector3> _truckWorkStations = _value.WorkStations;

            Transform _routeTransform = GameObject.Find(_routeName).transform;
            
            Vector3 _routePosition = _routeTransform.Find(_routeName + "/Waypoint-0").transform.position;
            
            Vector3 _position = new Vector3(_routePosition.x, 0f, _routePosition.z);

            CreateTruck(_truckName, _routeName, _truckWorkStations);
        }

    }
}