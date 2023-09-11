using System.Collections;
using System.Collections.Generic;
using UnityEngine;
#if UNITY_EDITOR
using UnityEditor;
#endif

namespace TrafficSimulation{
    public class ExitPlayMode : MonoBehaviour
    {
        public int nowTruckCount = 0;
        public int totalTruckCount;

        private SaveFile saveFile;

        public int _currentFileCount;
        public int _totalFileCount = WholeProcess.totalFileCount;

        void Start()
        {
            GameObject.Find("Roads").AddComponent<SaveFile>();

            saveFile = GetComponent<SaveFile>();
        }

        // Update is called once per frame
        void Update()
        {
            _currentFileCount = WholeProcess.currentFileCount;
            
            if(CompareCount(_currentFileCount, _totalFileCount))
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