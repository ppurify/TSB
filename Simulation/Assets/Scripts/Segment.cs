// Traffic Simulation
// https://github.com/mchrbn/unity-traffic-simulation

using System.Collections.Generic;
using UnityEngine;

namespace TrafficSimulation {
    // Class representing a road segment in the traffic simulation.
    public class Segment : MonoBehaviour {
        public List<Segment> nextSegments; // List of segments connected to this one.

        [HideInInspector] public int id; // Unique identifier for the segment.
        [HideInInspector] public List<Waypoint> waypoints; // List of waypoints in the segment.

        // Checks if a given position is on the segment.
        public bool IsOnSegment(Vector3 _p) {
            TrafficSystem ts = GetComponentInParent<TrafficSystem>();

            // Calculate distances between waypoints and the given position to determine if it's on the segment.
            for (int i = 0; i < waypoints.Count - 1; i++) {
                float d1 = Vector3.Distance(waypoints[i].transform.position, _p);
                float d2 = Vector3.Distance(waypoints[i + 1].transform.position, _p);
                float d3 = Vector3.Distance(waypoints[i].transform.position, waypoints[i + 1].transform.position);
                float a = (d1 + d2) - d3;

                // Use a threshold for distance calculation to determine if the position is on the segment.
                if (a < ts.segDetectThresh && a > -ts.segDetectThresh)
                    return true;
            }
            return false;
        }
    }
}
