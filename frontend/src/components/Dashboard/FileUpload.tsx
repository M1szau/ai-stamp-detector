import { MdOutlineFileUpload } from "react-icons/md";

export default function FileUpload() {
    return (
        <>
            <div className="w-fit h-fit items-center justify-center m-auto border-4 border-dashed border-blue-400 rounded-2xl px-20 py-10 mt-8">
                <div className="flex items-center justify-center text-center">
                    <MdOutlineFileUpload color={"gray"} size={150} />
                </div>

                <div className="flex flex-col items-center justify-center text-center mt-4">
                    <p className="text-2xl font-semibold mb-2">Drag & drop your PDF file here or click to browse</p>
                    <p className="text-xl text-gray-500 mb-4">Supported formats: PDF</p>
                    <button className="mt-4 px-4 py-2 bg-blue-500 text-white text-2xl rounded-3xl hover:bg-blue-600">Browse Files</button>
                </div>
            </div>
        </>
    );
}