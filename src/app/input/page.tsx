'use client'
import React, { useState, useEffect } from 'react';

const ImageUpload: React.FC = () => {
  const [selectedFile1, setSelectedFile1] = useState<File | null>(null);
  const [selectedFile2, setSelectedFile2] = useState<File | null>(null);
  const [previewURL1, setPreviewURL1] = useState<string | null>(null);
  const [previewURL2, setPreviewURL2] = useState<string | null>(null);
  const [result1, setResult1] = useState<string | null>(null);
  const [result2, setResult2] = useState<string | null>(null);
  const [comparisonResult, setComparisonResult] = useState<number | null>(null);


  const apiUrl = process.env.NEXT_PUBLIC_API_URL;

  const handleComparison = () => {
    if (result1 && result2) {
      console.log(JSON.stringify({
        expected: result1,
        student: result2,
      }))
      // Make an API request to compare the two results
      fetch(`${apiUrl}/compare/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          expected: result1,
          student: result2,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data.total_marks);
          setComparisonResult(data.total_marks);
        });
    }
  };


  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>, index: number) => {
    if (event.target.files && event.target.files[0]) {
      const file = event.target.files[0];
      if (index === 1) {
        setSelectedFile1(file);
      } else if (index === 2) {
        setSelectedFile2(file);
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        if (index === 1) {
          setPreviewURL1(e.target?.result as string);
        } else if (index === 2) {
          setPreviewURL2(e.target?.result as string);
        }
      };
      reader.readAsDataURL(file);
    }
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>, index: number) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (index === 1) {
      setSelectedFile1(file);
    } else if (index === 2) {
      setSelectedFile2(file);
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      if (index === 1) {
        setPreviewURL1(e.target?.result as string);
      } else if (index === 2) {
        setPreviewURL2(e.target?.result as string);
      }
    };
    reader.readAsDataURL(file);
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
  };

  useEffect(() => {
    if (selectedFile1) {
      const formData = new FormData();
      formData.append('file', selectedFile1);

      fetch(`${apiUrl}/upload`, {
        method: 'POST',
        body: formData,
      })
        .then((response) => response.json())
        .then((data:any) => {
          console.log(data)
          setResult1(data.summary_text);
        });
    }
  }, [selectedFile1, apiUrl]);

  useEffect(() => {
    if (selectedFile2) {
      const formData = new FormData();
      formData.append('file', selectedFile2);

      fetch(`${apiUrl}/uploadT`, {
        method: 'POST',
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data.summary_text)
          setResult2(data.summary_text);
        });
    }
  }, [selectedFile2, apiUrl]);

  const handleUpload = (index: number) => {
    if (index === 1 && selectedFile1) {
      setResult1('Uploading...');
    }
    if (index === 2 && selectedFile2) {
      setResult2('Uploading...');
    }
  };

  return (
    <div>
      <div className="flex">
        {Array.from([1, 2]).map((index) => (
          <div
            key={index}
            className="group rounded-lg border-2 border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30 m-2"
            onDrop={(event) => handleDrop(event, index)}
            onDragOver={handleDragOver}
          >
            {index === 1 ? (
              selectedFile1 ? (
                <img
                  src={previewURL1}
                  alt="Preview 1"
                  className="max-w-full h-auto"
                />
              ) : (
                <p className={`mb-3 text-2xl font-semibold`}>Drag & Drop or select an image</p>
              )
            ) : (
              selectedFile2 ? (
                <img
                  src={previewURL2}
                  alt="Preview 2"
                  className="max-w-full h-auto"
                />
              ) : (
                <p className={`mb-3 text-2xl font-semibold`}>Drag & Drop or select an image</p>
              )
            )}
            <input
              type="file"
              accept="image/*"
              onChange={(event) => handleFileChange(event, index)}
              className="m-2"
            />
            <button
              onClick={() => handleUpload(index)}
              className="m-2 bg-blue-500 text-white py-2 px-4 rounded-md"
            >
              Upload {index}
            </button>
            {index === 1 && result1 && (
              <div className="text-center mt-2 bg-gray-800 border rounded px-5 ">{result1}</div>
            )}
            {index === 2 && result2 && (
              <div className="text-center mt-2 bg-gray-800 border rounded px-5 ">{result2}</div>
            )}
          </div>
        ))}
      </div>
      <div className="mt-8 text-center">
        <button
          onClick={handleComparison}
          className="bg-blue-500 text-white py-2 px-4 rounded-md"
        >
          Compare Results
        </button>
        {comparisonResult !== null && (
          <div className="text-center mt-4">
            <p>Comparison Result: {comparisonResult}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ImageUpload;
