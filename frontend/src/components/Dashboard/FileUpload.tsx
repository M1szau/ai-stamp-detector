import { MdOutlineFileUpload } from "react-icons/md";
import { useState, useRef } from "react";

const API_URL = "http://localhost:5000";

interface DetectionResult {
    bbox: number[];
    confidence: number;
    class: string;
    class_id: number;
}

interface PageResult {
    page_number: number;
    stamps_count: number;
    detections: DetectionResult[];
}

interface UploadResponse {
    message: string;
    filename: string;
    has_stamps: boolean;
    total_stamps: number;
    total_pages: number;
    pages?: PageResult[];
    annotated_paths?: string[];
    detections?: DetectionResult[];
    annotated_path?: string;
}

export default function FileUpload() {
    const [file, setFile] = useState<File | null>(null);
    const [dragActive, setDragActive] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [uploadStatus, setUploadStatus] = useState<string | null>(null);
    const [results, setResults] = useState<UploadResponse | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleBrowseClick = () => {
        fileInputRef.current?.click();
    };

    const handleFileSelect = (selectedFile: File) => {
        //Validate file extension
        const validExtension = selectedFile.name.toLowerCase().endsWith(".pdf");
        
        //Validate MIME type
        const validMimeType = selectedFile.type === "application/pdf";
        
        //Validate file size (max 50MB)
        const maxFileSize = 50 * 1024 * 1024;
        const validFileSize = selectedFile.size > 0 && selectedFile.size <= maxFileSize;
        
        if (!validExtension) {
            alert("Error: File must have a .pdf extension");
            return;
        }
        
        if (!validMimeType) {
            alert("Error: File must be a valid PDF document");
            return;
        }
        
        if (!validFileSize) {
            if (selectedFile.size === 0) {
                alert("Error: File is empty");
            } else {
                alert("Error: File size must be less than 50MB");
            }
            return;
        }
        
        setFile(selectedFile);
        setUploadStatus(null);
        setResults(null); 
        console.log("File selected:", selectedFile.name, "Size:", selectedFile.size);
    };

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files?.[0]) {
            handleFileSelect(e.target.files[0]);
        }
    };

    const handleDrag = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        
        if (e.dataTransfer.files?.[0]) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!file) {
            alert("Please select a file first");
            return;
        }

        setIsLoading(true);
        setUploadStatus("Processing...");
        setResults(null);

        try {
            const formData = new FormData();
            formData.append("file", file);
            formData.append("confidence", "0.25"); // Default confidence threshold

            const response = await fetch(`${API_URL}/api/upload`, {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `Upload failed: ${response.statusText}`);
            }

            const data: UploadResponse = await response.json();
            setResults(data);
            
            if (data.has_stamps) {
                setUploadStatus(`Success! Found ${data.total_stamps} stamp${data.total_stamps > 1 ? 's' : ''} in ${data.total_pages} page${data.total_pages > 1 ? 's' : ''}`);
            } else {
                setUploadStatus("No stamps detected in the document");
            }
            
            console.log("Detection results:", data);
        } catch (error) {
            console.error("Upload error:", error);
            setUploadStatus(`Error: ${error instanceof Error ? error.message : "Unknown error"}`);
            setResults(null);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <>
            <div
                className={`w-fit h-fit items-center justify-center m-auto border-4 border-dashed rounded-2xl px-20 py-10 mt-8 transition-colors ${
                    dragActive ? "border-blue-600 bg-blue-50" : "border-blue-400"
                }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
            >
                <div className="flex items-center justify-center text-center">
                    <MdOutlineFileUpload color={"gray"} size={150} />
                </div>

                <div className="flex flex-col items-center justify-center text-center mt-4">
                    <p className="text-2xl font-semibold mb-2">
                        {file ? `File: ${file.name}` : "Drag & drop your PDF file here or click to browse"}
                    </p>
                    <p className="text-xl text-gray-500 mb-4">Supported formats: PDF</p>
                    <button
                        onClick={handleBrowseClick}
                        className="mt-4 px-4 py-2 bg-blue-500 text-white text-2xl rounded-3xl hover:bg-blue-600"
                    >
                        Browse Files
                    </button>
                    {file && (
                        <button
                            onClick={handleUpload}
                            disabled={isLoading}
                            className="mt-4 px-6 py-2 bg-green-500 text-white text-2xl rounded-3xl hover:bg-green-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
                        >
                            {isLoading ? "Processing..." : "Analyze Document"}
                        </button>
                    )}
                    {uploadStatus && (
                        <p className={`mt-4 text-lg font-semibold ${
                            uploadStatus.includes("Error") ? "text-red-500" : 
                            uploadStatus.includes("No stamps") ? "text-yellow-600" : 
                            "text-green-500"
                        }`}>
                            {uploadStatus}
                        </p>
                    )}
                    <input
                        ref={fileInputRef}
                        type="file"
                        accept=".pdf"
                        onChange={handleInputChange}
                        className="hidden"
                    />
                </div>
            </div>

            {/* Results Display */}
            {results && results.has_stamps && (
                <div className="max-w-6xl m-auto mt-8 p-6 bg-white rounded-lg shadow-lg">
                    <h2 className="text-3xl font-bold mb-4 text-center text-green-600">
                        ✓ Stamps Detected
                    </h2>
                    <p className="text-center text-xl mb-6">
                        Found {results.total_stamps} stamp{results.total_stamps > 1 ? 's' : ''} across {results.total_pages} page{results.total_pages > 1 ? 's' : ''}
                    </p>

                    {/* Display annotated images */}
                    <div className="space-y-6">
                        {results.annotated_paths && results.annotated_paths.map((path, index) => {
                            const filename = path.split('\\').pop() || path.split('/').pop();
                            const pageNum = results.pages?.[index]?.page_number || index + 1;
                            const stampsOnPage = results.pages?.[index]?.stamps_count || 0;
                            
                            return (
                                <div key={index} className="border rounded-lg p-4 bg-gray-50">
                                    <h3 className="text-xl font-semibold mb-2">
                                        Page {pageNum} - {stampsOnPage} stamp{stampsOnPage > 1 ? 's' : ''} detected
                                    </h3>
                                    <img
                                        src={`${API_URL}/api/results/${filename}`}
                                        alt={`Page ${pageNum} with detected stamps`}
                                        className="w-full rounded border border-gray-300"
                                        onError={(e) => {
                                            console.error('Failed to load image:', filename);
                                            e.currentTarget.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg"/>';
                                        }}
                                    />
                                    
                                    {/* Show detection details */}
                                    {results.pages?.[index]?.detections && (
                                        <div className="mt-3">
                                            <h4 className="font-semibold text-lg">Detection Details:</h4>
                                            <ul className="list-disc list-inside mt-2">
                                                {results.pages[index].detections.map((det, detIdx) => (
                                                    <li key={detIdx} className="text-gray-700">
                                                        Stamp #{detIdx + 1}: Confidence {(det.confidence * 100).toFixed(1)}%
                                                    </li>
                                                ))}
                                            </ul>
                                        </div>
                                    )}
                                </div>
                            );
                        })}

                        {/* For single image files */}
                        {results.annotated_path && (
                            <div className="border rounded-lg p-4 bg-gray-50">
                                <h3 className="text-xl font-semibold mb-2">
                                    Detected {results.total_stamps} stamp{results.total_stamps > 1 ? 's' : ''}
                                </h3>
                                <img
                                    src={`${API_URL}/api/results/${results.annotated_path.split('\\').pop() || results.annotated_path.split('/').pop()}`}
                                    alt="Detected stamps"
                                    className="w-full rounded border border-gray-300"
                                />
                                
                                {results.detections && (
                                    <div className="mt-3">
                                        <h4 className="font-semibold text-lg">Detection Details:</h4>
                                        <ul className="list-disc list-inside mt-2">
                                            {results.detections.map((det, detIdx) => (
                                                <li key={detIdx} className="text-gray-700">
                                                    Stamp #{detIdx + 1}: Confidence {(det.confidence * 100).toFixed(1)}%
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                )}
                            </div>
                        )}
                    </div>
                </div>
            )}

            {/* No stamps detected message */}
            {results && !results.has_stamps && (
                <div className="max-w-4xl m-auto mt-8 p-6 bg-yellow-50 rounded-lg shadow-lg border-2 border-yellow-400">
                    <h2 className="text-3xl font-bold mb-2 text-center text-yellow-700">
                        ⚠ No Stamps Detected
                    </h2>
                    <p className="text-center text-xl text-gray-700">
                        The document was analyzed but no stamps were found.
                    </p>
                    <p className="text-center text-gray-600 mt-2">
                        Analyzed {results.total_pages} page{results.total_pages > 1 ? 's' : ''}
                    </p>
                </div>
            )}
        </>
    );
}