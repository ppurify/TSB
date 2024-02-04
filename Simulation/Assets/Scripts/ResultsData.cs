using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// A ScriptableObject class representing result data.
[System.Serializable]
public class ResultsData : ScriptableObject
{
    // Property representing the file path.
    public string FilePath { get; private set; }
    // Property representing vehicle information.
    public string Vehicle { get; private set; }
    // Property representing route information.
    public string Route { get; private set; }
    // Property representing the origin point.
    public Vector3 Origin { get; private set; }
    // Property representing the destination point.
    public Vector3 Destination { get; private set; }
    // Property representing the path length.
    public float Path_length { get; private set; }
    // Property representing completion time when alone.
    public float CompletionTime_alone { get; private set; }
    // Property representing the total completion time.
    public float CompletionTime { get; private set; }
    // Property representing a list containing each stopwatch time.
    public List<float> StopwathTimeList { get; private set; }

    // Method to create result data.
    public void CreateResultData(string _filePath, string _vehicle, string _route, Vector3 _origin, Vector3 _destination, float _path_length, float _completionTime_alone, float _completionTime, List<float> _stopwathTimeList)
    {
        // Initialize properties with the provided values.
        FilePath = _filePath;
        Vehicle = _vehicle;
        Route = _route;
        Origin = _origin;
        Destination = _destination;
        Path_length = _path_length;
        CompletionTime_alone = _completionTime_alone;
        CompletionTime = _completionTime;
        StopwathTimeList = _stopwathTimeList;
    }
}