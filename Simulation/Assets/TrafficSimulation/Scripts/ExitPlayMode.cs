using System.Collections;
using System.Collections.Generic;
using UnityEngine;
#if UNITY_EDITOR
using UnityEditor;
#endif

namespace TrafficSimulation{
    public class ExitPlayMode : MonoBehaviour
    {
        public int nowTruckCount;
        public int totalTruckCount;

        private SaveFile saveFile;

        void Start()
        {
            nowTruckCount = 0;
            if(CreateTruckAndStation.isTwoFile)
            {
                totalTruckCount = CreateTruckAndStation.truckDataList_1.Count + CreateTruckAndStation.truckDataList_2.Count;
            }
            
            else
            {
                totalTruckCount = CreateTruckAndStation.truckDataList_1.Count;
            }

            GameObject.Find("Roads").AddComponent<SaveFile>();

            saveFile = GetComponent<SaveFile>();
        }

        // Update is called once per frame
        void Update()
        {
            if(CompareTruckCount(nowTruckCount, totalTruckCount))
            {   
                List<ResultsData> dataList = SaveFile.resultsDataList;
     
                foreach(ResultsData resultsData in dataList)
                {
                    saveFile.SaveToCSV(resultsData.FilePath, resultsData.Vehicle, resultsData.Route, resultsData.Origin, resultsData.Destination, resultsData.TotalTime, resultsData.StopwathTimeList);
                    UnityEngine.Debug.Log("Save " + resultsData.FilePath + "  --> " + resultsData.Vehicle + " data");
                }

                Debug.Log("Exit Play Mode");
                EditorApplication.ExitPlaymode();

#if UNITY_EDITOR
                AssetDatabase.Refresh();
#endif
            }

        }

        public bool CompareTruckCount(int _nowTruckCount, int _totalTruckCount)
        {
            return _nowTruckCount == _totalTruckCount;
        }
    }
}