using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System;
using UnityEngine;
using System.Linq;

namespace TrafficSimulation{
    public class SaveFile : MonoBehaviour
    {
        // 파일 저장 위치
        public string csvFileName;
        public string filePath;

        public static List<ResultsData> resultsDataList;
        private WholeProcess wholeProcess;
        private float cMax_prev;
        private float cMax_now;
        private float cMax;
        private float congestionRatio_avg_prev;
        private float congestionRatio_avg_now;
        private float congestionRatio_avg;
        private float totalCraneProcessTime;
        private bool isFirstLine;
        private string newLine;

        void Start()
        {
            totalCraneProcessTime = CranesInfo.quayCraneProcessTime + CranesInfo.yardCraneProcessTime;
        }

        public void SaveToCSV()
        {
            if(resultsDataList == null)
            {
                UnityEngine.Debug.LogError("resultsDataList is null !!");
            }

            else
            {
                UnityEngine.Debug.Log("resultsDataList.Count : " + resultsDataList);
                cMax = resultsDataList.Max(data => data.CompletionTime);
                congestionRatio_avg = congestionRatio_AVG(resultsDataList);

                // Get maxCompletionTime of less than Truk-100
                // Filter the dataList based on the condition isPrevTruck() == true
                var prevTruckDatas = resultsDataList.Where(data => isPrevTruck(data.Vehicle)).ToList();
                if (prevTruckDatas.Count > 0)
                {
                    // Find the maximum CompletionTime among the filtered results
                    cMax_prev = prevTruckDatas.Max(data => data.CompletionTime);
                    congestionRatio_avg_prev = congestionRatio_AVG(prevTruckDatas);
                }

                else
                {
                    UnityEngine.Debug.LogError("No prev trucks found in the dataList.");
                }

                var nowTruckDatas = resultsDataList.Where(data => !isPrevTruck(data.Vehicle)).ToList();
                if(nowTruckDatas.Count > 0)
                {
                    cMax_now = nowTruckDatas.Max(data => data.CompletionTime);
                    congestionRatio_avg_now = congestionRatio_AVG(nowTruckDatas);
                }

                else
                {
                    UnityEngine.Debug.LogError("No now trucks found in the dataList.");
                }
                
                isFirstLine = true;
                foreach(ResultsData data in resultsDataList)
                {   
                    float completionTime_byDistance = data.CompletionTime/data.Path_length;
                    AddLine(data.FilePath, data.Vehicle, data.Route, data.Origin, data.Destination, data.CompletionTime_alone, data.CompletionTime, completionTime_byDistance, data.StopwathTimeList, isFirstLine);
                    isFirstLine = false;
                }
            }
        }

        public void AddLine(string _filePath, string _truckName, string _routeName, Vector3 _origin, Vector3 _destination, float _completionTime_alone, float _completionTime, float _completionTime_byDistance, List<float> _arrivalTimeList, bool _isFirstLine)
        {   
            // Check if the CSV file exists
            if(!File.Exists(_filePath))
            {
                // Create a new CSV file and write the data
                using (StreamWriter sw = File.CreateText(_filePath))
                {   
                    string header = "Truck_id,Route_id,Origin,Destination,Completion_Time_alone,Completion_Time,Congestion_ratio,CompletionTime_by_Distance,PickupSta_AT,DropSta_AT,,,C_max_prev,C_max_now,C_max,Congestion_ratio_AVG_prev,Congestion_ratio_AVG_now,Congestion_ratio_AVG";
               
                    // Write the header and data to the CSV file
                    sw.WriteLine(header);
                }
            }

            // Read the existing content of the CSV file
            string[] lines = File.ReadAllLines(_filePath);

            // Convert the List<float> to a comma-separated string
            string arrivalTimeValues = string.Join(",", _arrivalTimeList);

            // Convert the Vector3 values to strings without including commas
            string originValue = _origin.ToString().Replace(",", string.Empty);
            string destinationValue = _destination.ToString().Replace(",", string.Empty);

            float congestionRatio = (_completionTime - _completionTime_alone) / (_completionTime_alone - totalCraneProcessTime);
            
            // Append the new data to the content
            if(_isFirstLine)
            {
                newLine = string.Format("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17}", _truckName, _routeName, originValue, destinationValue, _completionTime_alone, _completionTime, congestionRatio,
                                            _completionTime_byDistance, _arrivalTimeList[0], _arrivalTimeList[1], string.Empty, string.Empty, cMax_prev, cMax_now, cMax, congestionRatio_avg_prev, congestionRatio_avg_now, congestionRatio_avg);
            }

            else
            {
                newLine = string.Format("{0},{1},{2},{3},{4},{5},{6},{7},{8}", _truckName, _routeName, originValue, destinationValue, _completionTime_alone, _completionTime, congestionRatio, _completionTime_byDistance, arrivalTimeValues);
            }

            // Append the new line to the CSV file
            File.AppendAllText(_filePath, newLine + "\n");
        }

        // public void SaveToCSV(string _filePath, string _truckName, string _routeName, Vector3 _origin, Vector3 _destination, float _completionTime_alone, float _completionTime, List<float> _arrivalTimeList, bool _isFirstLine)
        // {
        //     // Check if the CSV file exists
        //     if(!File.Exists(_filePath))
        //     {
        //         // Create a new CSV file and write the data
        //         using (StreamWriter sw = File.CreateText(_filePath))
        //         {   
        //             string header = "Truck_id,Route_id,Origin,Destination,Completion_Time_alone,Completion_Time,Congestion_ratio,PickupSta_AT,DropSta_AT,,,C_max_prev,C_max_now,C_max,Congestion_ratio_AVG_prev,Congestion_ratio_AVG_now,Congestion_ratio_AVG";
               
        //             // Write the header and data to the CSV file
        //             sw.WriteLine(header);
        //         }
        //     }

        //     // Read the existing content of the CSV file
        //     string[] lines = File.ReadAllLines(_filePath);

        //     // Convert the List<float> to a comma-separated string
        //     string arrivalTimeValues = string.Join(",", _arrivalTimeList);

        //     // Convert the Vector3 values to strings without including commas
        //     string originValue = _origin.ToString().Replace(",", string.Empty);
        //     string destinationValue = _destination.ToString().Replace(",", string.Empty);

        //     float congestionRatio = ((_completionTime - 300) - (_completionTime_alone - 300)) / (_completionTime_alone - 300);
        //     UnityEngine.Debug.Log("congestionRatio : " + congestionRatio);
            
        //     // Append the new data to the content
        //     if(_isFirstLine)
        //     {
        //         string newLine = firstLine(_truckName, _routeName, originValue, destinationValue, _completionTime_alone, _completionTime, congestionRatio, _arrivalTimeList, 
        //                                                             _cMax_prev, _cMax_now, _cMax, _congestionRatio_avg_prev, _congestionRatio_avg_now, _congestionRatio_avg);
        //     }

        //     else
        //     {
        //         string newLine = string.Format("{0},{1},{2},{3},{4},{5},{6},{7}", _truckName, _routeName, originValue, destinationValue, _completionTime_alone, _completionTime, congestionRatio, arrivalTimeValues);
        //     }

        //     // Append the new line to the CSV file
        //     File.AppendAllText(_filePath, newLine + "\n");
        // }

        private bool isPrevTruck(string _vehicleName)
        {   
            bool _isPrevTruck = true;

            string[] parts = _vehicleName.Split('-');

            if(parts.Length == 2)
            {
                string numberString= parts[1];
                // Now, you can parse the numberString to get the integer value
                int truckIndex = int.Parse(numberString);

                if(truckIndex >= 100)
                {
                    _isPrevTruck = false; 
                }
            }

            else
            {
                UnityEngine.Debug.Log("Invalid vehicle format. Expected format: 'Truck-X'");
            }

            return _isPrevTruck;
        }

        private float congestionRatio_AVG(List<ResultsData> _dataList)
        {
            float totalCongestionRatio = 0;

            foreach(ResultsData data in _dataList)
            {
                float congestionRatio = (data.CompletionTime - data.CompletionTime_alone) / (data.CompletionTime_alone - totalCraneProcessTime);
                totalCongestionRatio += congestionRatio;
            }

            return totalCongestionRatio / _dataList.Count;
        }

    }
}