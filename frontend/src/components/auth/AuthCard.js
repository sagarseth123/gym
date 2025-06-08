// frontend/src/components/auth/AuthCard.js
import React from 'react';
// Optional: Import a Google icon if you have one as an SVG component
// import { GoogleIcon } from './icons';

const AuthCard = ({ activeTab, onTabChange, children }) => {
  const tabButtonBaseStyle = "w-1/2 py-3 text-sm font-medium leading-5 text-center focus:outline-none transition-colors duration-150 ease-in-out";
  const activeTabStyle = "bg-indigo-600 text-white shadow-lg";
  const inactiveTabStyle = "bg-gray-200 text-gray-700 hover:bg-gray-300";

  const handleGoogleSignInClick = () => {
    console.log('Google Sign-In button clicked (not functional yet)');
    // Future: Initiate Google OAuth flow
  };

  return (
    // space-y-6 will apply to direct children: Header Div, Tabs Div, Children Wrapper Div, Divider Div, Google Button Div
    <div className="w-full max-w-md bg-white p-6 sm:p-8 space-y-6 shadow-xl rounded-2xl">

      {/* Card Header */}
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900">
          GymVerse Unite
        </h1>
        <p className="mt-2 text-sm text-gray-600">
          Your fitness journey starts here
        </p>
      </div>

      {/* Tab Switching UI */}
      <div className="flex rounded-lg overflow-hidden border border-gray-300">
        <button
          onClick={() => onTabChange('signin')}
          className={`${tabButtonBaseStyle} rounded-l-lg ${activeTab === 'signin' ? activeTabStyle : inactiveTabStyle}`}
          aria-pressed={activeTab === 'signin'}
        >
          Sign In
        </button>
        <button
          onClick={() => onTabChange('signup')}
          className={`${tabButtonBaseStyle} rounded-r-lg ${activeTab === 'signup' ? activeTabStyle : inactiveTabStyle}`}
          aria-pressed={activeTab === 'signup'}
        >
          Sign Up
        </button>
      </div>

      {/* Render children (which will be the SignInForm or SignUpForm) */}
      {/* The prompt example had an extra div with mt-6 here, but space-y-6 on parent should handle it.
          If children (forms) need specific margins not covered by parent's space-y, they can add it themselves.
          For instance, if children is directly a form, form's own top margin might be 0 due to space-y.
          The current SignInForm/SignUpForm have "space-y-6" on the form element itself, which handles internal spacing.
          The 'mt-6' from the prompt example for the children wrapper is effectively handled by parent's 'space-y-6'.
      */}
      <div>
        {children}
      </div>

      {/* Divider */}
      <div className="relative flex py-3 items-center"> {/* Adjusted py-3 from py-5 from prompt */}
        <div className="flex-grow border-t border-gray-300"></div>
        <span className="flex-shrink mx-4 text-gray-400 text-xs uppercase">
          Or continue with
        </span>
        <div className="flex-grow border-t border-gray-300"></div>
      </div>

      {/* Social Sign-In Button (Google) */}
      <div>
        <button
          type="button"
          onClick={handleGoogleSignInClick}
          className="w-full inline-flex items-center justify-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          {/* Placeholder for Google Icon - an SVG would be better */}
          <svg className="w-5 h-5 mr-2 -ml-1" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path fillRule="evenodd" clipRule="evenodd" d="M48 24C48 22.044 47.8408 20.1373 47.5305 18.2941H24.48V28.6176H37.8183C37.2288 31.9412 35.5547 34.7059 32.9012 36.549V42.7059H40.9088C45.3958 38.7059 48 31.9412 48 24Z" fill="#4285F4"/>
            <path fillRule="evenodd" clipRule="evenodd" d="M24.4799 48.0001C31.0076 48.0001 36.4032 45.8824 39.9011 42.7059L32.9011 36.5491C30.7204 38.0001 27.8502 38.8236 24.4799 38.8236C17.8918 38.8236 12.262 34.353 10.4002 28.2353H2.16016V34.5295C5.65809 41.6471 14.2762 48.0001 24.4799 48.0001Z" fill="#34A853"/>
            <path fillRule="evenodd" clipRule="evenodd" d="M10.4002 28.2352C9.94736 26.8823 9.68259 25.4117 9.68259 23.9999C9.68259 22.5881 9.94736 21.1176 10.4002 19.7646V13.4705H2.16016C0.792743 16.2352 0 19.9411 0 23.9999C0 28.0587 0.792743 31.7646 2.16016 34.5293L10.4002 28.2352Z" fill="#FBBC05"/>
            <path fillRule="evenodd" clipRule="evenodd" d="M24.4799 9.17639C28.2899 9.17639 31.2394 10.5882 32.9011 12.1176L40.1412 4.88228C36.4032 1.76463 31.0076 -0.00012207 24.4799 -0.00012207C14.2762 -0.00012207 5.65809 6.35286 2.16016 13.4705L10.4002 19.7646C12.262 13.6469 17.8918 9.17639 24.4799 9.17639Z" fill="#EA4335"/>
          </svg>
          Sign in with Google
        </button>
      </div>
    </div>
  );
};

export default AuthCard;
