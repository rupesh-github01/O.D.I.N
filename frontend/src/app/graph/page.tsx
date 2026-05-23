"use client";

import { useEffect, useState } from "react";

import ReactFlow, {
  Background,
  Controls,
  Node,
  Edge
} from "reactflow";

import "reactflow/dist/style.css";

import api from "@/lib/api";

export default function GraphPage() {

const [nodes, setNodes] = useState<Node[]>([]);
const [edges, setEdges] = useState<Edge[]>([]);

  useEffect(() => {

    async function fetchGraph() {

      const response = await api.post(
        "/graph/explore",
        {
          concept: "Transformers"
        }
      );

      const related =
        response.data.related_concepts;

      const graphNodes:Node[] = [
        {
          id: "Transformers",
          position: { x: 250, y: 50 },
          data: {
            label: "Transformers"
          }
        }
      ];

      const graphEdges:Edge[] = [];

      related.forEach(
        (item: any, index: number) => {

          graphNodes.push({
            id: item.concept,
            position: {
              x: index * 200,
              y: 250
            },
            data: {
              label: item.concept
            }
          });

          graphEdges.push({
            id:
              `e-${index}`,

            source:
              "Transformers",

            target:
              item.concept,

            label:
              item.relationship
          });
        }
      );

      setNodes(graphNodes);

      setEdges(graphEdges);
    }

    fetchGraph();

  }, []);

  return (
    <div style={{
      width: "100vw",
      height: "100vh"
    }}>

      <ReactFlow
        nodes={nodes}
        edges={edges}
      >

        <Background />

        <Controls />

      </ReactFlow>

    </div>
  );
}