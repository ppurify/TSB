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

    // 각 QC, YC의 작업 시간 (Inspector 창에서 확인용)
    public float craneProcessTime;

    // QC 위치
    private float quayCranePosition_z = 200f;

    // QC, YC의 작업 시간
    public static float quayCraneProcessTime = 150f;
    public static float yardCraneProcessTime = 150f;

    void Awake()
    {
        craneStatus = 0;

        AssignCraneCapacity(quayCranePosition_z, 100, 100);

        AssignProcessTime(quayCranePosition_z, quayCraneProcessTime, yardCraneProcessTime);
        // craneCapacity = 2;
    
        processQueueList = new List<GameObject>();
        processList = new List<GameObject>();
        finishedQueueList_toLeft = new List<GameObject>();
        finishedQueueList_toRight = new List<GameObject>();
    }

    // QC, YC의 작업 시간을 할당
    private void AssignProcessTime(float quayCranePos_z, float _quayCraneProcessTime, float _yardCraneProcessTime)
    {
        // Assign process time to each crane
        if(this.transform.position.z == quayCranePos_z)
        {
            craneProcessTime = _quayCraneProcessTime;
        }

        else
        {
            craneProcessTime = _yardCraneProcessTime;
        }
    }
    
    // QC, YC의 한번에 작업 가능한 트럭 수를 할당
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