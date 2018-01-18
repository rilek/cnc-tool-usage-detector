import fs from 'fs';
import watch from 'node-watch';
import cp from 'child_process';
import c from '../config/config';


const textStream = fs.createWriteStream(c["textLogPath"], {flags: 'a'});
const htmlStream = fs.createWriteStream(c["htmlLogPath"], {flags: 'a'});


export const addLogRow = (sockets) => {
  const sendLog = sockets ?
                    (log) => sockets.emit("new_log", log) :
                    () => {};
  return (rawText, color, omitNewLine) => {
    const timestamp = omitNewLine !== true ? createTimestamp() : "";
    const linebreak = omitNewLine !== true ? "\r\n" : "";
    const text = color ? setColor(rawText, color) : rawText;
    const logRow = linebreak + (timestamp ? setColor(timestamp, "gray") : "") + text;
    const line = linebreak + timestamp + rawText;

    process.stdout.write(line);
    textStream.write(line);
    htmlStream.write(logRow);
    sendLog(logRow);
    return logRow;
  }
};

export const setColor = (text, color) =>
  '<span style="color: ' + c['colors'][color] + '">' + text + '</span>';

export const timeout = (ms) =>
  new Promise(resolve => setTimeout(resolve, ms));

export const createTimestamp = () =>
  "[" + new Date().toISOString() + "]: ";

export const getClassStr = (cls) => {
  console.log(cls);
  if(cls === 1)
    return "Tępe";
  else
    return "Ostre";
}