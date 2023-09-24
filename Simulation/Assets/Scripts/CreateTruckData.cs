using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class CreateTruckData : ScriptableObject
{
    public string Name { get; private set; }
    public string Route { get; private set; }
    public float CompletionTime_alone { get; private set; }
    public List<Vector3> WorkStations { get; private set; }
    
    public void CreateData(string name, string route, float _completionTime_alone, List<Vector3> stations)
    {
        Name = name;
        Route = route;
        CompletionTime_alone = _completionTime_alone;
        WorkStations = stations; 
    }
}
