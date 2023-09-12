using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
public class CreateRoad : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        CreateRoads();
    }

    public void CreateRoads()
    {
        string nodeFilePath =  "C:\\Users\\USER\\정화\\LAB\\TSB\\static Data\\Node Data_1.csv";

        // Read csv file
        using (StreamReader reader = new StreamReader(nodeFilePath))
        {
            // Skip the first line
            reader.ReadLine();

            while (!reader.EndOfStream)
            {
                string line = reader.ReadLine();
                string[] fields = line.Split(',');

                // Check if the row has at least two columns
                if (fields.Length >= 3)
                {
                    string axis_x = fields[1];
                    string axis_z = fields[2];

                    Vector3 road_pos = new Vector3(float.Parse(axis_x), 0.0f, float.Parse(axis_z));
                    // Debug.Log($"Road position: {road_pos}");

                    //Instantiate Road prefab
                    Instantiate(Resources.Load("side") as GameObject, road_pos, Quaternion.identity);
                }
            }
        }
    }
}
