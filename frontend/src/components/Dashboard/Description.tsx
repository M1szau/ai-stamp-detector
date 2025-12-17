import Box from "./Box.tsx"

import { IoDocumentAttachSharp } from "react-icons/io5";
import { MdAutoAwesome } from "react-icons/md";
import { FaCheckCircle } from "react-icons/fa";


export default function Description() {
    return (
        <>
            <div className="flex flex-col w-fit h-fit items-center justify-center m-auto p-4">
                <p className="text-xl font-bold mb-4">How it works?</p>
                <div className="flex flex-row gap-4">
                    <Box icon={<IoDocumentAttachSharp />} title="Upload Image" description="Upload a document in PDF format" iconColor="bg-blue-400"/>
                    <Box icon={<MdAutoAwesome />} title="AI Analysis" description="Our AI analyzes the stamp authenticity" iconColor="bg-violet-400"/>
                    <Box icon={<FaCheckCircle />} title="Get Results" description="Receive verification results almost instantly" iconColor="bg-green-400"/>
                </div>

            </div>
        </>
    );
}