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
        public int _currentFileCount;
        public int _totalFileCount;
        private SaveFile saveFile;
        private WholeProcess wholeProcess;
        
        // Update is called once per frame
        void Update()
        {   
            // _currentFileCount = WholeProcess.currentFileCount;
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