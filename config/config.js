const rootFolder = __dirname + "/../";

export default {
  textLogPath: rootFolder + "logs/text.log",
  htmlLogPath: rootFolder + "logs/html.log",
  rootFolder: rootFolder,
  tmpFilesFolder: rootFolder + "tmp_files",
  featuresApi: "http://localhost:8082",
  clasifierApi: "http://localhost:8080",
  colors: {
    green: "green",
    red: "red",
    gray: "gray",
    blue: "blue",
    yellow: "rgb(214, 193, 49)"
  }
}