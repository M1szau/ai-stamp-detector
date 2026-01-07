import { MdOutlineFileUpload } from "react-icons/md";
import { useState, useRef } from "react";

const API_URL = "http://localhost:5000";

export default function FileUpload() {
    const [file, setFile] = useState<File | null>(null);
    const [dragActive, setDragActive] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [uploadStatus, setUploadStatus] = useState<string | null>(null);
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
        setUploadStatus("Uploading...");

        try {
            const formData = new FormData();
            formData.append("file", file);

            const response = await fetch(`${API_URL}/api/upload`, {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Upload failed: ${response.statusText}`);
            }

            const data = await response.json();
            setUploadStatus("Upload successful!");
            console.log("Server response:", data);
            
            //Optional: Reset file after successful upload
            setTimeout(() => {
                setFile(null);
                setUploadStatus(null);
            }, 2000);
        } catch (error) {
            console.error("Upload error:", error);
            setUploadStatus(`Error: ${error instanceof Error ? error.message : "Unknown error"}`);
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
                            {isLoading ? "Uploading..." : "Upload to Server"}
                        </button>
                    )}
                    {uploadStatus && (
                        <p className={`mt-4 text-lg font-semibold ${uploadStatus.includes("Error") ? "text-red-500" : "text-green-500"}`}>
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
        </>
    );
}