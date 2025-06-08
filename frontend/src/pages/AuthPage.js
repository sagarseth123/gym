// frontend/src/pages/AuthPage.js
import React, { useState } from 'react';
import AuthCard from '../components/auth/AuthCard.js';
import SignInForm from '../components/auth/SignInForm.js';
import SignUpForm from '../components/auth/SignUpForm.js'; // Import SignUpForm

const AuthPage = () => {
  const [activeTab, setActiveTab] = useState('signin'); // 'signin' or 'signup'

  // Function to pass to AuthCard to change tabs, will be used later
  const handleTabChange = (tab) => {
    setActiveTab(tab);
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-sky-100 via-sky-200 to-sky-300 py-12 px-4 sm:px-6 lg:px-8">
      <AuthCard activeTab={activeTab} onTabChange={handleTabChange}>
        {activeTab === 'signin' ? <SignInForm /> : <SignUpForm />}
      </AuthCard>
    </div>
  );
};

export default AuthPage;
