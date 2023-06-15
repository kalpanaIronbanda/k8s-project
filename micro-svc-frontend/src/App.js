import React, { useState, useEffect } from 'react';

function App() {
  const [studentTable, setStudentTable] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(process.env.BACKEND_URL);
        const result = await response.text();
        setStudentTable(result);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <>
      <h1>Welcome to the Student List</h1>
      <div dangerouslySetInnerHTML={{ __html: studentTable }} />
    </>
  );
}

export default App;
