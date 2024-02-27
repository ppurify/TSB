using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using UnityEngine.SceneManagement;
using System.Text.RegularExpressions;

namespace TrafficSimulation {    
    public class WholeProcess : MonoBehaviour
    {
        // parameters

        // 상위 폴더 이름
        private static string caseName = "Modify_prior_congestion";
        // 상위 폴더 경로
        private string caseFolderPath = "Assets/Data/" + caseName;

        // YT 최대 작업 완료 시간
        public float limitTotalTime = 500f;

        // 차량 한대씩 돌리는 지 여부
        private bool _isOnebyOne = false;

        // --------------------------------------------------------
        
        // 한대씩 돌릴 때 이전 스케줄링 대상 폴더를 실행할 지 여부
        public bool isPrevFolder = true;
        private string prevFolderPath;
        private string nowFolderPath;

        
        public static bool playAgain = false;


        private List<string> prevRouteFileList = new List<string>();
        private List<string> prevTruckFileList = new List<string>();
        private List<string> nowRouteFileList = new List<string>();
        private List<string> nowTruckFileList = new List<string>();

        
        private string[] folderList;
        public int folderCount;
        public int currentFolderCount;

        private int prevFileCount;
        private int nowFileCount;
        
        public int subFolderCount;
        public int currentFileCount;
        public int totalFileCount;

        // ChangeToRotate Parameters
        private static float x1;
        private static float x2;
        private static float x3;
        private static float x4;

        private static float z1;
        private static float z2;
        private static float z3;
        private static float z4;

        //  corner, intersection Positions
        private static List<Vector3> cornerPositions = new List<Vector3>{new Vector3(0,0,0), new Vector3(750,0,0), new Vector3(750,0,200), new Vector3(0,0,200)};
        private static List<Vector3> intersectionPositions = new List<Vector3>
                                                                {
                                                                    new Vector3(250, 0, 0),
                                                                    new Vector3(500, 0, 0),
                                                                    new Vector3(0, 0, 50),
                                                                    new Vector3(250, 0, 50),
                                                                    new Vector3(500, 0, 50),
                                                                    new Vector3(750, 0, 50),
                                                                    new Vector3(0, 0, 100),
                                                                    new Vector3(250, 0, 100),
                                                                    new Vector3(500, 0, 100),
                                                                    new Vector3(750, 0, 100),
                                                                    new Vector3(0, 0, 150),
                                                                    new Vector3(250, 0, 150),
                                                                    new Vector3(500, 0, 150),
                                                                    new Vector3(750, 0, 150),
                                                                    new Vector3(250, 0, 200),
                                                                    new Vector3(500, 0, 200)
                                                                };

        public string currentPrevRouteFilePath;
        private string currentPrevTruckFilePath;
        public string currentNowRouteFilePath;
        private string currentNowTruckFilePath;

        
        // Route Parameters
        // private static List<List<Vector3>> routes = new List<List<Vector3>>();
        
        private static Dictionary<int, List<Vector3>> prevRouteDictionary = new Dictionary<int, List<Vector3>>();
        private static Dictionary<int, List<Vector3>> nowRouteDictionary = new Dictionary<int, List<Vector3>>();
        
        private static float route_Pos_y = 1.5f;
        private static Vector3 newPoint;
        
        private static int routePlusNum;
        
        // 이차선 도로를 위해 route를 이동시키는 scale
        private static float routeMoveScale = 5.5f;
        private static bool isRotate;        
        private static Vector3 newRoPoint;

        private static TrafficSystem wps;
        
        // 차량 생성 딜레이
        private float createTruckDelay = 1f;
        
        private CreateTruckAndStation createTruckAndStation;
        private ExitPlayMode exitPlayMode;
        private SaveFile saveFile;


        // Start is called before the first frame update
        void Awake()
        {
            if (Directory.Exists(caseFolderPath))
            {
                // 폴더 내의 하위 폴더 목록을 가져옵니다.
                folderList = Directory.GetDirectories(caseFolderPath);
                folderCount = folderList.Length;
                if (folderCount > 0)
                {
                    CreateTruckAndStation.isOneByOne = _isOnebyOne;
                    createTruckAndStation = GetComponent<CreateTruckAndStation>();
                    exitPlayMode = GetComponent<ExitPlayMode>();
                }

                else
                {
                    Debug.LogError("There is no folderList");
                }
            }
        }

        void Start()
        {
            GameObject.Find("Roads").AddComponent<SaveFile>();
            saveFile = GetComponent<SaveFile>();
            currentFileCount = 0;
            currentFolderCount = 0;
            Process();
        }

        void Update()
        {
            if(playAgain == true)
            {
                playAgain = false;
                Debug.Log("----------Again Process-----------");
                ReloadScene();
            }
        }

        private void GetPrevNowFolderPath(string _folderName)
        {
            // Use regular expressions to match "prev_" and "now_" followed by numbers
            Match prevMatch = Regex.Match(_folderName, @"prev_\d+");
            Match nowMatch = Regex.Match(_folderName, @"now_\d+");

            if (prevMatch.Success)
            {
                prevFolderPath = Path.Combine(_folderName, prevMatch.Value);
            }

            if(nowMatch.Success)
            {
                nowFolderPath = Path.Combine(_folderName, nowMatch.Value);
            }
        }

        public void ReloadScene()
        {
            // Get the current scene's name
            string currentSceneName = SceneManager.GetActiveScene().name;

            // Reload the current scene
            SceneManager.LoadScene(currentSceneName);
        }

        public void Process()
        {   
            subFolderCount = 0;
            GetPrevNowFolderPath(folderList[currentFolderCount]);
            
            CheckFolderCount();
            CreateTruckAndStation.subFolderCount = subFolderCount;

            currentPrevRouteFilePath = prevRouteFileList[currentFileCount];
            currentPrevTruckFilePath = prevTruckFileList[currentFileCount];
            
            currentNowRouteFilePath = nowRouteFileList[currentFileCount];
            currentNowTruckFilePath = nowTruckFileList[currentFileCount];

            string currenFilePath = SetSaveFileName();

            //  이미 결과 파일이 존재하는 경우
            if(File.Exists(currenFilePath))
            {
                currentFileCount++;
                Debug.Log("File already exists : " + saveFile.filePath);

                //  현재 폴더의 모든 파일을 돌았을 때
                if(currentFileCount == totalFileCount)
                {
                    Debug.Log("----- Next Folder ------");
                    currentFolderCount ++;
                    currentFileCount = 0;
                }

                //  모든 폴더를 돌았을 때
                if(currentFolderCount == folderCount)
                {
                    Debug.Log("----- End Process ------");
                }

                // 폴더가 남아있는 경우
                else
                {
                    Process();
                }
            }

            //  결과 파일이 존재하지 않는 경우
            else
            {
                // 경로 생성
                CreateAllRoutes();

                exitPlayMode.nowTruckCount = 0;

                //  createTruckDelay 후에 차량 생성
                Invoke("CreateTruck", createTruckDelay);
            }
        }

        //  result 파일 이름 설정
        private string SetSaveFileName()
        {
            // if(CreateTruckAndStation.isTwoFile)
            if(!_isOnebyOne)
            {
                saveFile.csvFileName = Path.GetFileName(currentPrevRouteFilePath) + "_with_" + Path.GetFileName(currentNowRouteFilePath);
            }

            else if(prevFolderPath != "")
            {
                saveFile.csvFileName = Path.GetFileName(currentPrevRouteFilePath);
            }
            
            else
            {
                saveFile.csvFileName = Path.GetFileName(currentNowRouteFilePath);
            }

            //  result file 저장 경로 설정
            string resultFolder = "Assets/Results/" + caseName +"/"+ Path.GetFileName(folderList[currentFolderCount]);

            //  result 폴더가 없는 경우 생성
            if (!Directory.Exists(resultFolder))
            {
             
                Directory.CreateDirectory(resultFolder);
            }

            if(CreateTruckAndStation.isOneByOne)
            {
                saveFile.filePath = resultFolder + "/result_NoCongestions_" + saveFile.csvFileName;
            }
            
            else
            {
                saveFile.filePath = resultFolder + "/result_" + saveFile.csvFileName;
            }

            return saveFile.filePath;
        }

        private void CreateTruck()
        {
            if(createTruckAndStation != null)
            {
                createTruckAndStation.CreatingTrucks(currentPrevTruckFilePath, currentNowTruckFilePath);

                if(subFolderCount == 2)
                {
                    exitPlayMode.totalTruckCount = CreateTruckAndStation.truckDataList_1.Count + CreateTruckAndStation.truckDataList_2.Count;
                }
                
                else if(prevFolderPath != "")
                {
                    exitPlayMode.totalTruckCount = CreateTruckAndStation.truckDataList_1.Count;
                }

                else if(nowFolderPath != "")
                {
                    exitPlayMode.totalTruckCount = CreateTruckAndStation.truckDataList_2.Count;
                }
            }
            else
            {
                Debug.LogError("createTruckAndStation is null");
            }
        }

        private void CheckFolderCount()
        {   
            List<string> routeFileList = new List<string>();
            List<string> truckFileList = new List<string>();
            
            //  차량 한대씩 돌리지 않고 다같이 돌리는 경우
            // if(!_isOnebyOne)
            if(prevFolderPath != "")
            {
                (routeFileList, truckFileList) = GetFileList(prevFolderPath);
                prevRouteFileList = routeFileList;
                prevTruckFileList = truckFileList;
                prevFileCount = prevRouteFileList.Count;

                subFolderCount++;
            }

            if(nowFolderPath != "")
            {
                (routeFileList, truckFileList) = GetFileList(nowFolderPath);
                nowRouteFileList = routeFileList;
                nowTruckFileList = truckFileList;
                nowFileCount = nowRouteFileList.Count;

                subFolderCount++;
            }
            
            if(prevFolderPath == "" & nowFolderPath == "")
            {
                Debug.LogError("Check Folder Path");
            }

            if(subFolderCount == 2)
            {
                CreateTruckAndStation.isTwoFile = true;
                totalFileCount = prevFileCount;
            }

            else
            {
                CreateTruckAndStation.isTwoFile = false;
                if(prevFileCount != 0)
                {
                    totalFileCount = prevFileCount;
                }

                else if(nowFileCount != 0)
                {
                    totalFileCount = nowFileCount;
                }
            }
        }

        private (List<string>, List<string>) GetFileList(string _folderPath)
        {   
            List<string> routeFileList = new List<string>();
            List<string> truckFileList = new List<string>();

            if(Directory.Exists(_folderPath))
            {
                // Get an array of all CSV files in the folder
                string[] csvFiles = Directory.GetFiles(_folderPath, "*.csv");

                foreach(string filePath in csvFiles)
                {
                    string fileName = Path.GetFileName(filePath);

                    if(fileName.Contains("RoutePoints"))
                    {
                        routeFileList.Add(filePath);
                    }

                    else
                    {
                        truckFileList.Add(filePath);
                    }
                }
            }

            else
            {
                Debug.LogError("Directory does not exist: " + _folderPath);
            }

            return (routeFileList, truckFileList);
        }

        // 모든 Route 생성
        private void CreateAllRoutes()
        {
            // 2개 파일 돌릴 때
            if(subFolderCount == 2)
            {
                prevRouteDictionary = CreateRouteList(currentPrevRouteFilePath);
                nowRouteDictionary = CreateRouteList(currentNowRouteFilePath);

                Debug.Log("Create prev Routes : " + currentPrevRouteFilePath + ", Create now Routes : " + currentNowRouteFilePath);

                if(prevRouteDictionary != null)
                {
                    CreateRoutes(currentPrevRouteFilePath, prevRouteDictionary, cornerPositions, intersectionPositions);
                }

                else
                {
                    Debug.LogError("prevRouteDictionary is null");    
                }

                if(nowRouteDictionary != null)
                {
                    CreateRoutes(currentNowRouteFilePath, nowRouteDictionary, cornerPositions, intersectionPositions);
                }

                else
                {
                    Debug.LogError("nowRouteDictionary is null");
                }
            }

            else if(subFolderCount == 1)
            {
                // 1개 파일 돌릴 때
                if(prevFileCount != 0)
                {
                    currentPrevRouteFilePath = prevRouteFileList[currentFileCount];
                    currentPrevTruckFilePath = prevTruckFileList[currentFileCount];
                    prevRouteDictionary = CreateRouteList(currentPrevRouteFilePath);

                    Debug.Log("Create prev Routes : " + currentPrevRouteFilePath);

                    if(prevRouteDictionary != null)
                    {
                        CreateRoutes(currentPrevRouteFilePath, prevRouteDictionary, cornerPositions, intersectionPositions);                    }

                    else
                    {
                        Debug.LogError("prevRouteDictionary is null");
                    }
                    
                }

                else if(nowFileCount != 0)
                {
                    currentNowRouteFilePath = nowRouteFileList[currentFileCount];
                    currentNowTruckFilePath = nowTruckFileList[currentFileCount];
                    nowRouteDictionary = CreateRouteList(currentNowRouteFilePath);

                    Debug.Log("Create now Routes : " + currentNowRouteFilePath);

                    if(nowRouteDictionary != null)
                    {
                        CreateRoutes(currentNowRouteFilePath, nowRouteDictionary, cornerPositions, intersectionPositions);
                    }

                    else
                    {
                        Debug.LogError("nowRouteDictionary is null");
                    }
                }
            }

            else
            {
                Debug.LogError("Check Folder Count");
            }
        }
        
        //  Route의 각 포인트를 리스트로 만들어 딕셔너리에 저장
        private static Dictionary<int, List<Vector3>> CreateRouteList(string _routefilePath)
        {   
            Dictionary<int, List<Vector3>> _routeDictionary = new Dictionary<int, List<Vector3>>();

            if (!File.Exists(_routefilePath))
            {
                Debug.LogError("File does not exist: " + _routefilePath);
            }

            else
            {
                using (StreamReader reader = new StreamReader(_routefilePath))
                {
                    // Skip the first line
                    reader.ReadLine();

                    // string line = reader.ReadLine();
                    string[] fields;

                    // routeNum과 리스트를 매핑할 딕셔너리
                    string line;
                    while ((line = reader.ReadLine()) != null)
                    {
                        fields = line.Split(',');

                        if (fields.Length == 4)
                        {
                            int routeNum = int.Parse(fields[0]);

                            if (!_routeDictionary.TryGetValue(routeNum, out List<Vector3> routePoints))
                            {
                                routePoints = new List<Vector3>();
                                _routeDictionary.Add(routeNum, routePoints);
                            }

                            float x = float.Parse(fields[1]);
                            float y = float.Parse(fields[2]);
                            float z = float.Parse(fields[3]);

                            Vector3 point = new Vector3(x, y, z);
                            routePoints.Add(point);

                        }
                    }
                }
            }
            

            return _routeDictionary;
        }                                               

        private static void CreateRoutes(string _routeFilePath, Dictionary<int, List<Vector3>> _routeDictionary, List<Vector3> _corners, List<Vector3> _intersections)
        {   
            GetPlusNum(_routeFilePath);
            
            List<Vector3> checkingRotateList = new List<Vector3>();
            
            if(_corners.Count > 0 && _intersections.Count > 0)
            {
                checkingRotateList.AddRange(_corners);
                checkingRotateList.AddRange(_intersections);
            }
            
            else
            {
                Debug.LogError("There is no corners or intersections");
            }

            string parentGOName = Path.GetFileName(_routeFilePath);
            GameObject parentGO = new GameObject(parentGOName);
            parentGO.transform.position = Vector3.zero;

            //  각 경로(segment) 생성
            foreach(int dict_key in _routeDictionary.Keys)
            {   
                List<Vector3> route = _routeDictionary[dict_key];

                if(route == null) Debug.LogError("route is null");

                int newRouteNum = dict_key + routePlusNum;
                string routeName = "Route-" + newRouteNum.ToString();
                
                GameObject mainGo = new GameObject(routeName);
                mainGo.transform.position = Vector3.zero;
                mainGo.transform.SetParent(parentGO.transform);

                mainGo.AddComponent<TrafficSystem>();
                mainGo.AddComponent<RouteInfo>();

                wps = mainGo.GetComponent<TrafficSystem>();
                RouteInfo routeInfo = mainGo.GetComponent<RouteInfo>();


                AddSegment(route[0], routeName);
                
                for(int p=0; p <route.Count; p++)
                {  
                    List<Vector3> newRotationPoints = new List<Vector3>();
                    List<Vector3> paths = new List<Vector3>();

                    // Debug.Log("routeName : " + routeName + ", route[p] : " + route[p]);
                    if(p > 0 && p+1 < route.Count)
                    {   
                        // 회전하는 위치인 경우
                        if(RotatePosition(route[p-1], route[p], route[p+1], checkingRotateList))
                        {
                            newRotationPoints = ChangeToRotate(route[p-1], route[p], route[p+1]);

                            // Debug.Log("routeName : " + routeName + ", route[p] : " + route[p] + " is rotate position");   
                            List<Vector3> rPoints = new List<Vector3>();

                            for(int rPoint = 0; rPoint <newRotationPoints.Count; rPoint++)
                            {   
                                if(rPoint+1 < newRotationPoints.Count)
                                {
                                    rPoints = EditPathPoints(newRotationPoints[rPoint], newRotationPoints[rPoint+1], routeMoveScale);

                                    newRoPoint = rPoints[0];
                                    newRoPoint.y = route_Pos_y;
                                    AddWaypoint(newRoPoint);
                                }

                                else
                                {
                                    newRoPoint = rPoints[1];
                                    newRoPoint.y = route_Pos_y;
                                    AddWaypoint(newRoPoint);
                                }
                            }
                        }

                        // 회전구간 아닌 경우
                        else
                        {   
                            // 다시 돌아가는 길인 경우
                            if(p-1 >= 0 && route[p-1] == route[p+1])
                            {   
                                // routeInfo.uTurnNum ++;
                                paths = EditPathPoints(route[p-1], route[p], routeMoveScale);
                                newPoint = paths[1];
                                newPoint.y = route_Pos_y;
                                AddWaypoint(newPoint);
                                routeInfo.uTurnStations.Add(route[p]);
                            }

                            paths = EditPathPoints(route[p], route[p+1], routeMoveScale);
                            newPoint = paths[0];
                            newPoint.y = route_Pos_y;
                            AddWaypoint(newPoint);
                            
                        }
                    }

                    // p = 0 or p+1 = route.Count
                    else
                    {   
                        if(p == 0)
                        {
                            paths = EditPathPoints(route[p], route[p+1], routeMoveScale);

                            newPoint = paths[0];
                            newPoint.y = route_Pos_y;
                            AddWaypoint(newPoint);
                        }
                        

                        if(p+1 == route.Count)
                        {   
                            paths = EditPathPoints(route[p-1], route[p], routeMoveScale);

                            newPoint = paths[1];
                            newPoint.y = route_Pos_y;
                            AddWaypoint(newPoint);
                        }
                    }
                }
            }
        }

        // now, prev 구분하기 위해 YT, route index에 routePlusNum 만큼 더하기
        private static void GetPlusNum(string _routefilePath)
        {   
            string fileName = Path.GetFileName(_routefilePath);
            
            if(fileName.Contains("now"))
            {
                routePlusNum = 100;
            }

            else if(fileName.Contains("prev"))
            {
                routePlusNum = 0;
            }
        }

        //  route를 _routeMovesacle만큼 이동시키기
        public static List<Vector3> EditPathPoints(Vector3 nowPoint, Vector3 nextPoint, float _routeMoveScale)
        {   
            float axis_x_next_now = nextPoint.x - nowPoint.x;
            float axis_z_next_now = nextPoint.z - nowPoint.z;

            List<Vector3> EditPoints = new List<Vector3>();

            if(axis_x_next_now < 0)
            {
                nowPoint.z += _routeMoveScale;
                nextPoint.z += _routeMoveScale;
            }

            else if(axis_x_next_now > 0)
            {
                nowPoint.z -= _routeMoveScale;
                nextPoint.z -= _routeMoveScale;
            }

            if(axis_z_next_now < 0)
            {
                nowPoint.x -= _routeMoveScale;
                nextPoint.x -= _routeMoveScale;
            }

            else if(axis_z_next_now > 0)
            {
                nowPoint.x += _routeMoveScale;
                nextPoint.x += _routeMoveScale;
            }

            EditPoints.Add(nowPoint);
            EditPoints.Add(nextPoint);

            return EditPoints;
        }

        // route의 각 포인트를 waypoint로 만들어 segment에 추가
        private static void AddWaypoint(Vector3 position) 
        {
            GameObject go = new GameObject("Waypoint-" + wps.curSegment.waypoints.Count);
            go.transform.SetParent(wps.curSegment.transform);
            go.transform.position = position;

            Waypoint wp = go.AddComponent<Waypoint>();
            wp.Refresh(wps.curSegment.waypoints.Count, wps.curSegment);

            //Record changes to the TrafficSystem (string not relevant here)
            wps.curSegment.waypoints.Add(wp);
        }

        // 각 경로 생성
        private static void AddSegment(Vector3 position, string routeName) 
        {
            int segId = wps.segments.Count;
            GameObject segGo = new GameObject(routeName);
            segGo.transform.SetParent(wps.transform);

            segGo.transform.position = position;

            wps.curSegment = segGo.AddComponent<Segment>();
            wps.curSegment.id = segId;
            wps.curSegment.waypoints = new List<Waypoint>();
            wps.curSegment.nextSegments = new List<Segment>();

            //Record changes to the TrafficSystem (string not relevant here)
            wps.segments.Add(wps.curSegment);
        }

        // 회전하는 위치(corner, intersection)인지 확인
        private static bool RotatePosition(Vector3 prePosition, Vector3 nowPosition, Vector3 nextPosition, List<Vector3> coordinateList)
        {   
            isRotate = CheckIfCoordinateExists(prePosition, nowPosition, nextPosition, coordinateList);
            return isRotate;
        }
        
        //  회전구간에서 회전할 포인트들의 위치를 변경
        private static List<Vector3> ChangeToRotate(Vector3 previousPoint, Vector3 nowPoint, Vector3 nextPoint)
        {   
            float nowPoint_x = nowPoint.x;
            float nowPoint_z = nowPoint.z;

            float axis_x_pre_now = previousPoint.x - nowPoint_x;
            float axis_x_next_now = nextPoint.x - nowPoint_x;

            float axis_z_pre_now = previousPoint.z - nowPoint_z;
            float axis_z_next_now = nextPoint.z - nowPoint_z;

            List<Vector3> rotatePoints = new List<Vector3>();
            
            if(axis_x_pre_now == 0 && axis_z_next_now == 0)
            {   
                if(axis_z_pre_now > 0)
                {
                    // Down Right (ㄴ 반대 모양)
                    if(axis_x_next_now < 0)
                    {
                        // Debug.Log(_routeName + " --> Down Right (ㄴ 반대 모양)");
                        x1 = nowPoint_x -1f;
                        z1 = nowPoint_z + 12.5f;

                        x2 = nowPoint_x - 4f;
                        z2 = nowPoint_z + 6.5f;

                        x3 = nowPoint_x - 8f;
                        z3 = nowPoint_z + 2.5f;

                        x4 = nowPoint_x - 14f;
                        z4 = nowPoint_z;
                    }

                    // Down Left (ㄴ 모양)
                    else if(axis_x_next_now > 0)
                    {                        
                        x1 = nowPoint_x + 2f;
                        z1 = nowPoint_z + 20f;

                        x2 = nowPoint_x + 6f;
                        z2 = nowPoint_z + 12.5f;

                        x3 = nowPoint_x + 13f;
                        z3 = nowPoint_z + 6.5f;

                        x4 = nowPoint_x + 20f;
                        z4 = nowPoint_z + 2.5f;
                    }
                }

                else if(axis_z_pre_now < 0)
                {
                    // Up left 2 (ㄱ 모양)
                    if(axis_x_next_now < 0)
                    {
                        x1 = nowPoint_x;
                        z1 = nowPoint_z - 25.5f;

                        x2 = nowPoint_x - 2f;
                        z2 = nowPoint_z - 15.5f;

                        x3 = nowPoint_x - 10f;
                        z3 = nowPoint_z - 6.5f;

                        x4 = nowPoint_x - 20f;
                        z4 = nowPoint_z;
                    }

                    // Up right 2(ㄱ 반대모양)
                    else if(axis_x_next_now > 0)
                    {
                        x1 = nowPoint_x;
                        z1 = nowPoint_z - 12.5f;

                        x2 = nowPoint_x + 3f;
                        z2 = nowPoint_z - 6.5f;

                        x3 = nowPoint_x + 8f;
                        z3 = nowPoint_z - 2.5f;

                        x4 = nowPoint_x + 15f;
                        z4 = nowPoint_z;

                    }
                    
                }
                
            }

            else if(axis_z_pre_now == 0 && axis_x_next_now == 0)
            {
                if(axis_z_next_now > 0)
                {
                    // Up left (ㄴ 반대 모양)
                    if(axis_x_pre_now < 0)
                    {   
                        // Debug.Log(_routeName + " --> Up left (ㄴ 반대 모양)");
                        x1 = nowPoint_x - 20f;
                        z1 = nowPoint_z;

                        x2 = nowPoint_x - 10f;
                        z2 = nowPoint_z + 6.5f;

                        x3 = nowPoint_x - 2f;
                        z3 = nowPoint_z + 15.5f;

                        x4 = nowPoint_x;
                        z4 = nowPoint_z + 25.5f;
                    }

                    // Up right (ㄴ 모양)
                    else if(axis_x_pre_now > 0)
                    {
                        // Debug.Log(_routeName + " --> Up right (ㄴ 모양)");
                        x1 = nowPoint_x + 15f;
                        z1 = nowPoint_z;
            
                        x2 = nowPoint_x + 8f;
                        z2 = nowPoint_z + 2.5f;

                        x3 = nowPoint_x + 3.5f;
                        z3 = nowPoint_z + 6.5f;

                        x4 = nowPoint_x;
                        z4 = nowPoint_z + 12.5f;
                    }
                }

                else if(axis_z_next_now < 0)
                {
                    // Down right 2 (ㄱ 모양)
                    if(axis_x_pre_now < 0)
                    {
                        // Debug.Log(_routeName + " --> Down right 2 (ㄱ 모양)");
                        x1 = nowPoint_x - 15f;
                        z1 = nowPoint_z;

                        x2 = nowPoint_x - 8f;
                        z2 = nowPoint_z - 2.5f;

                        x3 = nowPoint_x - 3f;
                        z3 = nowPoint_z - 6.5f;

                        x4 = nowPoint_x;
                        z4 = nowPoint_z - 12.5f;
                    }

                    // Down left 2 (ㄱ 반대 모양)
                    else if(axis_x_pre_now > 0)
                    {
                        // Debug.Log(_routeName + " --> Down left 2 (ㄱ 반대 모양)");
                        x1 = nowPoint_x + 20f;
                        z1 = nowPoint_z - 2f;

                        x2 = nowPoint_x + 13f;
                        z2 = nowPoint_z - 6.5f;

                        x3 = nowPoint_x + 6.5f;
                        z3 = nowPoint_z - 13f;

                        x4 = nowPoint_x + 2f;
                        z4 = nowPoint_z - 22f;
                    }

                    
                }
                
            }

            // 자연스럽게 회전하기 위해 회전 포인트 추가
            rotatePoints.Add(new Vector3(x1, 0f, z1));
            rotatePoints.Add(new Vector3(x2, 0f, z2));
            rotatePoints.Add(new Vector3(x3, 0f, z3));
            rotatePoints.Add(new Vector3(x4, 0f, z4));

            return rotatePoints;
        }
        
        // corner, intersection에서 회전을 해야하는 지 확인
        private static bool CheckIfCoordinateExists(Vector3 prePo, Vector3 nowPo, Vector3 nextPo, List<Vector3> coordinateList)
        {   
            float pre_now_x = prePo.x - nowPo.x;
            float pre_now_z = prePo.z - nowPo.z;
            float now_next_x = nowPo.x - nextPo.x;
            float now_next_z = nowPo.z - nextPo.z;

            bool case_1 = pre_now_x == 0 && pre_now_z != 0 && now_next_x != 0 && now_next_z == 0;
            bool case_2 = pre_now_x != 0 && pre_now_z == 0 && now_next_x == 0 && now_next_z != 0;

            bool isExist = coordinateList.Contains(nowPo) && (case_1 || case_2);
            return isExist;
        }
    
    }
}