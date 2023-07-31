using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CranesInfo : MonoBehaviour
{

    // 현재 작업 중인 트럭 개수
    public int craneStatus;
    // 작업 가능한 Max 트럭 개수
    public int craneCapacity;

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
        craneStatus = 0;
        // Randomly assign 2 or 3 to the 'craneCapacity' variable
        // craneCapacity = Random.Range(2, 4);
        AssignCraneCapacity(quayCranePosition_z, 3, 2);

        AssignProcessTime(quayCranePosition_z);
        // craneCapacity = 2;
    
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
            craneProcessTime = 80f;
            // craneProcessTime = 127f;
        }

        else
        {
            craneProcessTime = 180f;
            // craneProcessTime = 90f;
        }
    }
    
    private void AssignCraneCapacity(float quayCranePos_z, int _quayCraneCapacity, int _yardCraneCapacity)
    {
        // Quay crane capacity
        if(this.transform.position.z == quayCranePos_z)
        {
            craneCapacity = _quayCraneCapacity;
        }

        // Yard crane capacity
        else
        {
            craneCapacity = _yardCraneCapacity;
        }
    }
}