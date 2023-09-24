using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class ResultsData : ScriptableObject
{
    public string FilePath { get; private set; }
    public string Vehicle { get; private set; }
    public string Route { get; private set; }
    public Vector3 Origin { get; private set; }
    public Vector3 Destination { get; private set; }
    public float CompletionTime_alone { get; private set; }
    public float CompletionTime { get; private set; }
    public List<float> StopwathTimeList { get; private set; }

    public void CreateResultData(string _filePath, string _vehicle, string _route, Vector3 _origin, Vector3 _destination, float _completionTime_alone, float _completionTime, List<float> _stopwathTimeList)
    {
        FilePath = _filePath;
        Vehicle = _vehicle;
        Route = _route;
        Origin = _origin;
        Destination = _destination;
        CompletionTime_alone = _completionTime_alone;
        CompletionTime = _completionTime;
        StopwathTimeList = _stopwathTimeList;
    }
  
}
