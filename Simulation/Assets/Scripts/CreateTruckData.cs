using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class CreateTruckData : ScriptableObject
{
    public string Name { get; private set; }
    public string Route { get; private set; }
    public float Path_length { get; private set; }
    public float CompletionTime_alone { get; private set; }
    public List<Vector3> WorkStations { get; private set; }
    
    public void CreateData(string name, string route, float _path_length, float _completionTime_alone, List<Vector3> stations)
    {
        Name = name;
        Route = route;
        Path_length = _path_length;
        CompletionTime_alone = _completionTime_alone;
        WorkStations = stations; 
    }
}
