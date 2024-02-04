using System.Collections;
using System.Collections.Generic;
using UnityEngine;


#if UNITY_EDITOR
using UnityEditor;
#endif

namespace TrafficSimulation{
    public class ExitPlayMode : MonoBehaviour
    {
        // Number of finished trucks 
        public int nowTruckCount;
        // Total number of trucks in the scene
        public int totalTruckCount;
        private SaveFile saveFile;
        private WholeProcess wholeProcess;
        
        void Start()
        {
            wholeProcess = GameObject.Find("Roads").GetComponent<WholeProcess>();
        }

        // Update is called once per frame
        // If the number of finished trucks is equal to the total number of trucks, exit play mode
        void Update()
        {   
            if(CompareCount(wholeProcess.folderCount, wholeProcess.currentFolderCount))
            {
                Debug.Log("Exit Play Mode");
                EditorApplication.ExitPlaymode();
            }

#if UNITY_EDITOR
                AssetDatabase.Refresh();
#endif
        }

        // Compare the number of finished trucks and the total number of trucks
        public bool CompareCount(int _nowCount, int _totalCount)
        {
            return _nowCount == _totalCount;
        }
    }
}