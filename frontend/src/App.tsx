import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Hero from './components/Hero';
import InputPanel from './components/InputPanel';
import AnalysisBoard from './components/AnalysisBoard';
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

export type Reasoning = {
  controlFlow: string[];
  dataFlow: string[];
};

export type AnalysisResponse = {
  changedElement?: string;
  impactedFunctions?: string[];
  impactedVariables?: string[];
  reasoning?: Reasoning;
  error?: string;
};

export default function App() {
  const [sourceCode, setSourceCode] = useState('');
  const [changedElementId, setChangedElementId] = useState('');
  const [analysisScope, setAnalysisScope] = useState('full');

  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState('');

  const handleDemoLoad = async () => {
    try {
      const res = await axios.get(`${API_BASE}/demo-data`);
      setSourceCode(res.data.code);
      setChangedElementId('func_getUser'); // preselect a demo change
    } catch (err) {
      console.error(err);
      setError("Failed to load demo data. Is backend running?");
    }
  };

  const handleAnalyze = async () => {
    if (!sourceCode.trim()) {
      setError("Source code is empty.");
      return;
    }
    if (!changedElementId.trim()) {
      setError("Please specify the changed element (e.g., func_getUser or func_authenticate).");
      return;
    }

    setIsAnalyzing(true);
    setError('');
    setResult(null);

    try {
      const res = await axios.post(`${API_BASE}/analyze`, {
        sourceCode: sourceCode,
        changedElementId: changedElementId.trim(),
        analysisScope: analysisScope
      });

      if (res.data.error) {
        setError(res.data.error);
      } else {
        setResult(res.data);
      }
    } catch (err: any) {
      setError(err.response?.data?.error || err.message || "Network Error: Could not reach the server.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-800 via-slate-900 to-black font-sans text-slate-200">

      {/* Header/Hero Section */}
      <Hero />

      <main className="w-full max-w-7xl px-4 sm:px-6 lg:px-8 py-8 flex flex-col gap-8 z-10">
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="p-4 bg-red-900/50 border border-red-500/50 rounded-xl text-red-200 flex items-center justify-between"
            >
              <span>{error}</span>
              <button onClick={() => setError('')} className="text-red-300 hover:text-white">&times;</button>
            </motion.div>
          )}
        </AnimatePresence>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">

          <div className="lg:col-span-4 flex flex-col gap-6">
            <InputPanel
              sourceCode={sourceCode} setSourceCode={setSourceCode}
              changedElementId={changedElementId} setChangedElementId={setChangedElementId}
              analysisScope={analysisScope} setAnalysisScope={setAnalysisScope}
              onAnalyze={handleAnalyze} isAnalyzing={isAnalyzing}
              onLoadDemo={handleDemoLoad}
            />
          </div>

          <div className="lg:col-span-8 flex flex-col h-[700px]">
            <AnalysisBoard result={result} isAnalyzing={isAnalyzing} />
          </div>

        </div>
      </main>

    </div>
  )
}
