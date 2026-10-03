import React, { useEffect, useState } from 'react';

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
    let mounted = true;

    const checkBackend = async () => {
      try {
        const data = await fetchHealth();

        if (!mounted) {
          return;
        }

        setBackendData(data);

        setBackendStatus(
          data.status === 'healthy'
            ? 'healthy'
            : 'degraded',
        );
      } catch (error) {
        if (!mounted) {
          return;
        }

        setBackendStatus('offline');
      }
    };

    checkBackend();

    const interval = setInterval(checkBackend, 15000);

    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-[#0A0F1D] text-slate-100">
      <Navbar
        activePage={activePage}
        setActivePage={setActivePage}
        backendStatus={backendStatus}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8">
        {activePage === 'home' && (
          <Home
            onNavigate={setActivePage}
            backendData={backendData}
          />
        )}

        {activePage === 'analyzer' && (
          <Analyzer
            backendStatus={backendStatus}
          />
        )}

        {activePage === 'history' && (
          <History
            backendData={backendData}
          />
        )}

        {activePage === 'awareness' && (
          <Awareness />
        )}
      </main>

      <Footer />
    </div>
  );
}
