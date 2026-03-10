// we'll use lucide icons uniformly
import { UploadCloud, Play, Search, FileCode2, Database } from 'lucide-react';
import { motion } from 'framer-motion';

export default function InputPanel({
    sourceCode, setSourceCode,
    changedElementId, setChangedElementId,
    analysisScope, setAnalysisScope,
    onAnalyze, isAnalyzing, onLoadDemo
}: any) {
    return (
        <div className="glass p-6 rounded-2xl flex flex-col gap-5 h-full relative overflow-hidden">

            {/* Optional decorative background */}
            <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 blur-[50px] rounded-full pointer-events-none" />

            <div>
                <h2 className="text-xl font-bold flex items-center gap-2 mb-2">
                    <FileCode2 className="w-5 h-5 text-indigo-400" />
                    Source Code
                </h2>
                <p className="text-sm text-slate-400 mb-4">
                    Paste your functions/classes below, or load the research demo data.
                </p>

                <div className="relative group">
                    <textarea
                        value={sourceCode}
                        onChange={(e) => setSourceCode(e.target.value)}
                        className="w-full h-48 bg-slate-900/80 border-2 border-slate-700/50 rounded-xl p-4 font-mono text-sm resize-none focus:outline-none focus:border-indigo-500/50 shadow-inner custom-scrollbar transition-colors"
                        placeholder="class DatabaseManager { ... }"
                    />
                    <button
                        onClick={onLoadDemo}
                        className="absolute top-3 right-3 text-xs bg-indigo-500/20 hover:bg-indigo-500/40 text-indigo-300 px-3 py-1.5 rounded-lg border border-indigo-500/30 transition-all flex items-center gap-1.5 backdrop-blur-sm"
                    >
                        <Database className="w-3.5 h-3.5" />
                        Load Demo Set
                    </button>
                </div>
            </div>

            <div className="h-px bg-slate-700/50 w-full" />

            <div>
                <h2 className="text-lg font-bold flex items-center gap-2 mb-3">
                    <Search className="w-4 h-4 text-violet-400" />
                    Change Specification
                </h2>

                <div className="flex flex-col gap-4">
                    <div>
                        <label className="block text-xs font-semibold text-slate-400 mb-1.5 uppercase tracking-wider">
                            Changed Element ID
                        </label>
                        <input
                            type="text"
                            value={changedElementId}
                            onChange={(e) => setChangedElementId(e.target.value)}
                            placeholder="e.g., func_getUser"
                            className="w-full bg-slate-900/80 border-2 border-slate-700/50 rounded-xl px-4 py-2.5 outline-none focus:border-violet-500/50 transition-colors placeholder:text-slate-600"
                        />
                    </div>

                    <div>
                        <label className="block text-xs font-semibold text-slate-400 mb-1.5 uppercase tracking-wider">
                            Analysis Scope
                        </label>
                        <select
                            value={analysisScope}
                            onChange={(e) => setAnalysisScope(e.target.value)}
                            className="w-full bg-slate-900/80 border-2 border-slate-700/50 rounded-xl px-4 py-2.5 outline-none focus:border-violet-500/50 transition-colors appearance-none cursor-pointer"
                        >
                            <option value="full">Full Semantic Impact</option>
                            <option value="call">Call Dependency (Control Flow)</option>
                            <option value="data">Data Dependency (Reads/Writes)</option>
                        </select>
                    </div>
                </div>
            </div>

            <div className="mt-auto pt-4">
                <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={onAnalyze}
                    disabled={isAnalyzing || !sourceCode.trim() || !changedElementId.trim()}
                    className={`w-full py-3.5 rounded-xl font-bold flex items-center justify-center gap-2 transition-all ${isAnalyzing || !sourceCode.trim() || !changedElementId.trim()
                            ? 'bg-slate-700 text-slate-400 cursor-not-allowed'
                            : 'bg-gradient-to-r from-indigo-500 to-violet-600 hover:from-indigo-400 hover:to-violet-500 text-white shadow-lg shadow-indigo-500/25'
                        }`}
                >
                    {isAnalyzing ? (
                        <div className="w-5 h-5 border-2 border-slate-400 border-t-transparent rounded-full animate-spin" />
                    ) : (
                        <>
                            <Play className="w-5 h-5 fill-current" />
                            Run Analysis
                        </>
                    )}
                </motion.button>
            </div>

        </div>
    );
}
