using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class StationsInfo : MonoBehaviour
{

    // 현재 작업 중인 트럭 개수
    public int stationStatus;
    // 작업 가능한 Max 트럭 개수
    public int stationCapacity;

    // 작업 대기 중인 트럭 리스트
    public List<GameObject> processQueueList;

    // 작업 중인 트럭 리스트
    public List<GameObject> processList;

    // 작업 끝난 트럭 리스트
    public List<GameObject> finishedQueueList_toLeft;
    public List<GameObject> finishedQueueList_toRight;

    public float craneProcessTime;
    private float quayCranePosition_z = 200f;


    void Awake()
    {
        stationStatus = 0;
        // Randomly assign 2 or 3 to the 'stationCapacity' variable
        stationCapacity = Random.Range(2, 4);

        AssignProcessTime(quayCranePosition_z);
        // stationCapacity = 2;
    
        processQueueList = new List<GameObject>();
        processList = new List<GameObject>();
        finishedQueueList_toLeft = new List<GameObject>();
        finishedQueueList_toRight = new List<GameObject>();
    }

    private void AssignProcessTime(float quayCranePos_z)
    {
        // Assign process time to each crane
        if(this.transform.position.z == quayCranePos_z)
        {
            craneProcessTime = 180f;
        }

        else
        {
            craneProcessTime = 120f;
        }
    }
    
}