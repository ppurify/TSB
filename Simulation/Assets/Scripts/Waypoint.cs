// Traffic Simulation
// https://github.com/mchrbn/unity-traffic-simulation

using UnityEngine;

namespace TrafficSimulation {
    // Class representing a waypoint in the traffic simulation.
    public class Waypoint : MonoBehaviour {
        [HideInInspector] public Segment segment; // Reference to the segment the waypoint belongs to.

        // Refreshes the waypoint with new information.
        public void Refresh(int _newId, Segment _newSegment) {
            segment = _newSegment;
            name = "Waypoint-" + _newId;
            tag = "Waypoint";
            
            // Set the layer to Default
            gameObject.layer = 0;
            
            // Remove the Collider as it is not necessary anymore
            RemoveCollider();
        }

        // Removes the SphereCollider component from the waypoint.
        public void RemoveCollider() {
            if (GetComponent<SphereCollider>()) {
                DestroyImmediate(gameObject.GetComponent<SphereCollider>());
            }
        }

        // Returns the visual position of the waypoint with a slight vertical offset.
        public Vector3 GetVisualPos() {
            return transform.position + new Vector3(0, 0.5f, 0);
        }
    }
}
