// Traffic Simulation
// https://github.com/mchrbn/unity-traffic-simulation


using System.Collections.Generic;
using UnityEngine;

namespace TrafficSimulation {
    // Class representing the main traffic system in the simulation.
    public class TrafficSystem : MonoBehaviour {
        public bool hideGuizmos = false;  // Controls whether to hide gizmos in the editor.
        public float segDetectThresh = 0.1f;  // Threshold for segment detection.
        public ArrowDraw arrowDrawType = ArrowDraw.ByLength;  // Type of arrow drawing for waypoints.
        public int arrowCount = 1;  // Number of arrows for waypoint visualization.
        public float arrowDistance = 5;  // Distance between arrows for waypoint visualization.
        public float arrowSizeWaypoint = 1;  // Size of arrows for waypoint visualization.
        public float arrowSizeIntersection = 0.5f;  // Size of arrows for intersection visualization.
        public float waypointSize = 0.5f;  // Size of waypoints.
        public string[] collisionLayers;  // Layers to consider for collision detection.
        
        public List<Segment> segments = new List<Segment>();  // List of segments in the traffic system.
        public List<Intersection> intersections = new List<Intersection>();  // List of intersections in the traffic system.
        public Segment curSegment = null;  // Current segment reference for the traffic system.
        
        // Gets all waypoints in the traffic system.
        public List<Waypoint> GetAllWaypoints() {
            List<Waypoint> points = new List<Waypoint>();

            foreach (Segment segment in segments) {
                points.AddRange(segment.waypoints);
            }

            return points;
        }

        // Saves the status of all intersections in the traffic system.
        public void SaveTrafficSystem(){
            Intersection[] its  = GameObject.FindObjectsOfType<Intersection>();
            foreach(Intersection it in its)
                it.SaveIntersectionStatus();
        }

        // Resumes the status of all intersections in the traffic system.
        public void ResumeTrafficSystem(){
            Intersection[] its  = GameObject.FindObjectsOfType<Intersection>();
            foreach(Intersection it in its)
                it.ResumeIntersectionStatus();
        }
    }

    // Enumeration for different types of arrow drawing.
    public enum ArrowDraw {
        FixedCount, ByLength, Off
    }
}
