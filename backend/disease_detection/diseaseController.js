// Import the 'path' and 'spawn' modules. 'spawn' is a built-in Node.js function.
const path = require('path');
const { spawn } = require('child_process');

// The main controller function
exports.detectDisease = (req, res) => {
  
  // --- 1. Define Paths and Arguments ---
  
  // The absolute path to your Python executable. This makes the code robust.
  // Make sure this path is correct for your system.
  const pythonExecutable = 'C:\\Users\\Dell\\AppData\\Local\\Programs\\Python\\Python311\\python.exe';
  
  // The absolute path to the Python script we want to run.
  const scriptPath = path.join(__dirname, 'predict.py');

  // The arguments to pass to the script: the uploaded image's path and the crop type.
  const args = [scriptPath, req.file.path, req.body.crop];
  
  console.log('Spawning Python process...');
  
  // --- 2. Spawn the Python Child Process ---
  // We launch Python and pass our script and arguments to it.
  const pythonProcess = spawn(pythonExecutable, args);

  // --- 3. Listen for Data (from Python's 'print' statements) ---
  
  let predictionData = '';
  // 'pythonProcess.stdout' is the output stream. We listen for 'data' events on it.
  pythonProcess.stdout.on('data', (data) => {
    // The data comes in as a buffer, so we convert it to a string and append it.
    predictionData += data.toString();
  });

  // --- 4. Listen for Errors ---
  
  let errorData = '';
  // 'pythonProcess.stderr' is the error stream. We listen for errors here.
  pythonProcess.stderr.on('data', (data) => {
    // We log any errors immediately to the console for debugging.
    console.error(`Python stderr: ${data}`);
    errorData += data.toString();
  });

  // --- 5. Handle the Process Exit ---
  
  // The 'close' event fires when the Python script has finished its execution.
  pythonProcess.on('close', (code) => {
    console.log(`Python process exited with code ${code}`);

    // A code of 0 means the script ran successfully. Any other code means an error occurred.
    if (code !== 0) {
      return res.status(500).json({ 
        error: 'Python script failed to execute.',
        details: errorData || 'Script exited with a non-zero code but no error message.'
      });
    }

    // If successful, send the collected prediction data back to the frontend.
    // We .trim() to remove any extra newlines from the Python print statement.
    res.status(200).json({ prediction: predictionData.trim() });
  });
};