# Frontend Documentation

This document outlines how to build the frontend using **React** and **Vite** for a fast development experience. It covers styling with **Tailwind CSS**, building UI components with **dfaisyui**, and handling real-time alerts with **Socket.io**.

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn

## Setup

1. **Create the Project with Vite and React**

    Run the following command to scaffold a new React project using Vite:
    ```
    npm create vite@latest my-react-app --template react
    cd my-react-app
    npm install
    ```

2. **Add Tailwind CSS**

    Install Tailwind CSS and its dependencies:
    ```
    npm install -D tailwindcss postcss autoprefixer
    npx tailwindcss init -p
    ```
    Configure your `tailwind.config.js`:
    ```js
    module.exports = {
      content: [
         "./index.html",
         "./src/**/*.{js,jsx,ts,tsx}",
      ],
      theme: {
         extend: {},
      },
      plugins: [],
    }
    ```
    Add the Tailwind directives to your CSS:
    ```css
    @tailwind base;
    @tailwind components;
    @tailwind utilities;
    ```

3. **Integrate dfaisyui Component Library**

    Install dfaisyui (if available as a package, otherwise refer to its documentation):
    ```
    npm install dfaisyui
    ```
    Import and configure it in your project (example in your main CSS or component file):
    ```js
    // In your main JS/JSX file or a dedicated configuration file
    import 'dfaisyui/dist/dfaisyui.css';
    ```

4. **Set Up Socket.io for Real-Time Alerts**

    Install Socket.io client:
    ```
    npm install socket.io-client
    ```
    Create a service or use it directly within your components. Example usage:
    ```jsx
    // src/components/RealTimeAlerts.jsx
    import React, { useEffect, useState } from 'react';
    import io from 'socket.io-client';

    const socket = io('http://your-server-address');

    function RealTimeAlerts() {
      const [alerts, setAlerts] = useState([]);

      useEffect(() => {
         socket.on('alert', (message) => {
            setAlerts((prevAlerts) => [...prevAlerts, message]);
         });

         return () => socket.off('alert');
      }, []);

      return (
         <div className="p-4">
            <h2 className="text-xl font-bold mb-4">Real-Time Alerts</h2>
            <ul>
              {alerts.map((alert, index) => (
                 <li key={index} className="mb-2">
                    {alert}
                 </li>
              ))}
            </ul>
         </div>
      );
    }

    export default RealTimeAlerts;
    ```
    Then, include your `RealTimeAlerts` component in the relevant part of your application.

## Running the Project

To start the development server, execute:
```
npm install
npm run dev
```
Vite will start the server, and you can open the application in your browser.

## Conclusion

This setup guides you through integrating **React**, **Vite**, **Tailwind CSS**, **dfaisyui**, and **Socket.io** for a dynamic and real-time frontend application. Further customization may be needed based on specific project requirements.

