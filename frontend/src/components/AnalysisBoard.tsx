import { useMemo } from 'react';
import { ReactFlow, Controls, Background, Panel } from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { motion } from 'framer-motion';
import { FileCode, ShieldAlert, GitCommitVertical } from 'lucide-react';
import dagre from 'dagre';

const dagreGraph = new dagre.graphlib.Graph();
dagreGraph.setDefaultEdgeLabel(() => ({}));

// Extracted positioning algorithm
const getLayoutedElements = (nodes: any[], edges: any[], direction = 'TB') => {
    const isHorizontal = direction === 'LR';
    dagreGraph.setGraph({ rankdir: direction });

    nodes.forEach((node) => {
        // Approx dimensions
        dagreGraph.setNode(node.id, { width: 180, height: 70 });
    });

    edges.forEach((edge) => {
        dagreGraph.setEdge(edge.source, edge.target);
    });

    dagre.layout(dagreGraph);

    const newNodes = nodes.map((node) => {
        const nodeWithPosition = dagreGraph.node(node.id);
        const newNode = {
            ...node,
            targetPosition: isHorizontal ? 'left' : 'top',
            sourcePosition: isHorizontal ? 'right' : 'bottom',
            position: {
                x: nodeWithPosition.x - 90,
                y: nodeWithPosition.y - 35,
            },
        };
        return newNode;
    });

    return { nodes: newNodes, edges };
};

export default function AnalysisBoard({ result, isAnalyzing }: { result: any, isAnalyzing: boolean }) {

    const { nodes, edges } = useMemo(() => {
        if (!result || result.error) return { nodes: [], edges: [] };

        const flowNodes: any[] = [];
        const flowEdges: any[] = [];

        // Adding root changed element
        const rootId = result.changedElement || "Unknown";

        // Find human readable name for root if it exists in the payloads
        let rootName = rootId;
        const rootFunc = (result.impactedFunctions || []).find((f: any) => f.id === rootId);
        const rootVar = (result.impactedVariables || []).find((v: any) => v.id === rootId);
        if (rootFunc) rootName = rootFunc.name;
        if (rootVar) rootName = rootVar.name;

        flowNodes.push({
            id: rootId,
            data: { label: `[CHANGED]\n${rootName}` },
            style: {
                background: 'linear-gradient(135deg, #ef4444 0%, #b91c1c 100%)',
                color: '#ffffff',
                border: 'none',
                borderRadius: '8px',
                padding: '12px',
                fontWeight: 'bold',
                boxShadow: '0 4px 16px rgba(239, 68, 68, 0.4)'
            }
        });

        // Add impacted functions
        (result.impactedFunctions || []).forEach((funcObj: { id: string, name: string }) => {
            if (funcObj.id !== rootId) {
                flowNodes.push({
                    id: funcObj.id,
                    data: { label: `ƒ ${funcObj.name}` },
                    style: {
                        background: '#1e293b',
                        color: '#a5b4fc',
                        border: '2px solid #6366f1',
                        borderRadius: '8px',
                        padding: '12px',
                        fontWeight: '600',
                        boxShadow: '0 4px 12px rgba(99, 102, 241, 0.2)'
                    }
                });
                flowEdges.push({
                    id: `${rootId}-${funcObj.id}`, source: rootId, target: funcObj.id, label: 'impacts', animated: true,
                    style: { stroke: '#818cf8', strokeWidth: 2 },
                    labelStyle: { fill: '#a5b4fc', fontWeight: 600 },
                    labelBgStyle: { fill: '#1e293b', opacity: 0.8 }
                });
            }
        });

        // Add impacted variables
        (result.impactedVariables || []).forEach((varObj: { id: string, name: string }) => {
            if (varObj.id !== rootId) {
                flowNodes.push({
                    id: varObj.id,
                    data: { label: `v ${varObj.name}` },
                    style: {
                        background: '#1e293b',
                        color: '#6ee7b7',
                        border: '2px solid #10b981',
                        borderRadius: '8px',
                        padding: '12px',
                        fontWeight: '600',
                        boxShadow: '0 4px 12px rgba(16, 185, 129, 0.2)'
                    }
                });
                flowEdges.push({
                    id: `${rootId}-${varObj.id}`, source: rootId, target: varObj.id, label: 'impacts', animated: true,
                    style: { stroke: '#34d399', strokeWidth: 2 },
                    labelStyle: { fill: '#6ee7b7', fontWeight: 600 },
                    labelBgStyle: { fill: '#1e293b', opacity: 0.8 }
                });
            }
        });

        // Use our customized dagre layout to place them
        return getLayoutedElements(flowNodes, flowEdges);
    }, [result]);

    if (isAnalyzing) {
        return (
            <div className="glass rounded-2xl flex items-center justify-center h-full">
                <div className="flex flex-col items-center gap-4 text-indigo-400">
                    <div className="w-12 h-12 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin" />
                    <p className="font-medium animate-pulse">Running Logic Inference Engine...</p>
                </div>
            </div>
        );
    }

    if (!result) {
        return (
            <div className="glass rounded-2xl flex flex-col items-center justify-center h-full border-dashed border-2 text-slate-500 gap-4">
                <FileCode className="w-12 h-12 opacity-50" />
                <p className="font-medium">Run analysis to view semantic impact graph</p>
            </div>
        );
    }

    const totalImpacted = (result.impactedFunctions?.length || 0) + (result.impactedVariables?.length || 0);
    const severityColor = totalImpacted > 10 ? 'text-red-400 bg-red-400/10 border-red-400/20' :
        totalImpacted > 3 ? 'text-amber-400 bg-amber-400/10 border-amber-400/20' :
            'text-emerald-400 bg-emerald-400/10 border-emerald-400/20';

    return (
        <div className="h-full flex flex-col gap-6">

            {/* Upper: The Graphical Visualizer */}
            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="glass rounded-2xl h-2/3 overflow-hidden relative border-2 border-slate-700/50"
            >
                <ReactFlow
                    nodes={nodes}
                    edges={edges}
                    fitView
                    className="bg-slate-900"
                    minZoom={0.5}
                    maxZoom={2}
                >
                    <Background color="#334155" gap={24} size={2} />
                    <Controls className="fill-slate-200 text-slate-900 bg-slate-800 border-slate-700" />

                    <Panel position="top-right">
                        <div className={`px-4 py-2 rounded-full border ${severityColor} font-bold text-sm shadow-xl flex items-center gap-2 backdrop-blur-md`}>
                            <ShieldAlert className="w-4 h-4" />
                            {totalImpacted} elements impacted
                        </div>
                    </Panel>
                </ReactFlow>
            </motion.div>

            {/* Lower: Explanation Engine output */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="glass rounded-2xl h-1/3 p-5 overflow-y-auto custom-scrollbar flex flex-col gap-3"
            >
                <h3 className="text-lg font-bold flex items-center gap-2 sticky top-0 bg-slate-800/90 backdrop-blur pb-2 z-10 border-b border-slate-700/50">
                    <GitCommitVertical className="w-5 h-5 text-indigo-400" />
                    Semantic Explanation Chain
                </h3>

                <div className="flex flex-col gap-2 pt-2">
                    <div className="text-sm font-bold text-slate-300 mt-2">Control Flow Dependencies</div>
                    {result.reasoning?.controlFlow?.length === 0 && <span className="text-xs text-slate-500">None detected.</span>}
                    {result.reasoning?.controlFlow?.map((reason: string, idx: number) => (
                        <div key={`cf-${idx}`} className="flex flex-col p-3 rounded-lg bg-slate-900/50 border border-slate-700/50 hover:bg-slate-700/30 transition-colors">
                            <div className="text-sm text-slate-400">{reason}</div>
                        </div>
                    ))}

                    <div className="text-sm font-bold text-slate-300 mt-2">Data Flow Dependencies</div>
                    {result.reasoning?.dataFlow?.length === 0 && <span className="text-xs text-slate-500">None detected.</span>}
                    {result.reasoning?.dataFlow?.map((reason: string, idx: number) => (
                        <div key={`df-${idx}`} className="flex flex-col p-3 rounded-lg bg-slate-900/50 border border-slate-700/50 hover:bg-slate-700/30 transition-colors">
                            <div className="text-sm text-slate-400">{reason}</div>
                        </div>
                    ))}
                </div>
            </motion.div>

        </div>
    );
}
