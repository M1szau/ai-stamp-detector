import type { ReactNode } from 'react';

interface BoxProps{
    icon: ReactNode;
    title: string;
    description: string;
    iconColor: string;
}

export default function Box({icon, title, description, iconColor}: BoxProps){
    return(
        <div className="flex flex-col w-64 h-48 shadow-lg bg-[#F6F5F5] rounded-2xl p-4 justify-center items-center text-center gap-2">
            <div className={`text-4xl rounded-full w-fit h-fit p-2 flex items-center justify-center text-white ${iconColor}`}>{icon}</div>
            <div className="text-lg font-bold">{title}</div>
            <div className="text-sm font-semibold text-gray-500">{description}</div>
        </div>
    );
}