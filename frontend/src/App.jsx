import React, { useState, useEffect } from 'react';
import Navbar from './components/layout/Navbar';
import Footer from './components/layout/Footer';
import Home from './pages/Home';
import Analyzer from './pages/Analyzer';
import History from './pages/History';
import Awareness from './pages/Awareness';
import { fetchHealth } from './api/client';

export default function App() {
  const [activePage, setActivePage] = useState('home');
  const [backendStatus, setBackendStatus] = useState('connecting');
  const [backendData, setBackendData] = useState(null);

  useEffect(() => {
    let isMounted = true;
    const checkBackend = async () => {
      try {
        const data = await fetchHealth();
        if (isMounted) {
          setBackendData(data);
          setBackendStatus(data.status === 'healthy' ? 'healthy' : 'degraded');
        }
      } catch (err) {
        if (isMounted) {
          console.warn('Backend connection unavailable:', err.message);
          setBackendStatus('offline');
        }
      }
    };

    checkBackend();
    const interval = setInterval(checkBackend, 15000);
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-[#0A0F1D] text-slate-100 cyber-grid">
      <Navbar
        activePage={activePage}
        setActivePage={setActivePage}
        backendStatus={backendStatus}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8">
        {activePage === 'home' && (
          <Home onNavigate={setActivePage} backendData={backendData} />
        )}
        {activePage === 'analyzer' && (
          <Analyzer backendStatus={backendStatus} />
        )}
        {activePage === 'history' && (
          <History backendData={backendData} />
        )}
        {activePage === 'awareness' && (
          <Awareness />
        )}
      </main>

      <Footer />
    </div>
  );
}
