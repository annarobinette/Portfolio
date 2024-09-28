import React, { useState } from 'react';
import { Settings } from 'lucide-react';

const AccessibilityPanel = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [fontSize, setFontSize] = useState('medium');
  const [contrast, setContrast] = useState('default');

  const togglePanel = () => setIsOpen(!isOpen);

  const changeFontSize = (size) => {
    setFontSize(size);
    document.body.style.fontSize = size === 'large' ? '18px' : '16px';
  };

  const changeContrast = (newContrast) => {
    setContrast(newContrast);
    if (newContrast === 'high') {
      document.body.classList.add('high-contrast');
    } else {
      document.body.classList.remove('high-contrast');
    }
  };

  return (
    <div className="fixed top-4 right-4 z-50">
      <button
        onClick={togglePanel}
        className="bg-blue-500 text-white p-2 rounded-full shadow-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
        title="Change accessibility settings"
      >
        <Settings size={24} />
      </button>
      
      {isOpen && (
        <div className="mt-2 p-4 bg-white rounded-lg shadow-xl border border-gray-200">
          <h2 className="text-lg font-semibold mb-2">Accessibility Settings</h2>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700">Font Size</label>
            <select
              value={fontSize}
              onChange={(e) => changeFontSize(e.target.value)}
              className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
            >
              <option value="medium">Medium</option>
              <option value="large">Large</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700">Contrast</label>
            <select
              value={contrast}
              onChange={(e) => changeContrast(e.target.value)}
              className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
            >
              <option value="default">Default</option>
              <option value="high">High Contrast</option>
            </select>
          </div>
        </div>
      )}
    </div>
  );
};

export default AccessibilityPanel;