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
        public static string csvFileName;
        public string filePath;

        public static List<ResultsData> resultsDataList = new List<ResultsData>();

        void Start()
        {
            if(CreateTruckAndStation.isTwoFile)
            {
                csvFileName = CreateTruckAndStation.truckFileName_1 + "-" + CreateTruckAndStation.truckFileName_2;
            }

            else
            {
                csvFileName = CreateTruckAndStation.truckFileName_1;
            }

            if(CreateTruckAndStation.isOneByOne)
            {
                filePath = "Assets/Results/result-NoCongestions-" + csvFileName;
            }
            
            else
            {
                filePath = "Assets/Results/result-" + csvFileName;
            }
        }

        public void SaveToCSV(string _filePath, string _truckName, string _routeName, Vector3 _origin, Vector3 _destination, float _totalTime, List<float> _arrivalTimeList)
        {
            // Check if the CSV file exists
            if(!File.Exists(_filePath))
            {
                // Create a new CSV file and write the data
                using (StreamWriter sw = File.CreateText(_filePath))
                {
                    string header = "Truck_id,Route_id,Origin,Destination,Total Time,PickupSta AT,DropSta AT";

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

            // Append the new data to the content
            string newLine = string.Format("{0},{1},{2},{3},{4},{5}", _truckName, _routeName, originValue, destinationValue, _totalTime, arrivalTimeValues);

            // Append the new line to the CSV file
            File.AppendAllText(_filePath, newLine + "\n");
        }
    }
}