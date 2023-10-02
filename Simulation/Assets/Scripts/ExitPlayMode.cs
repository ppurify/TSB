using System.Collections;
using System.Collections.Generic;
using UnityEngine;


#if UNITY_EDITOR
using UnityEditor;
#endif

namespace TrafficSimulation{
    public class ExitPlayMode : MonoBehaviour
    {
        public int nowTruckCount;
        public int totalTruckCount;
        private SaveFile saveFile;
        private WholeProcess wholeProcess;
        
        void Start()
        {
            wholeProcess = GameObject.Find("Roads").GetComponent<WholeProcess>();
        }

        // Update is called once per frame
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

        public bool CompareCount(int _nowCount, int _totalCount)
        {
            return _nowCount == _totalCount;
        }
    }
}