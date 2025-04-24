const path = require('path');
const { spawn } = require('child_process');

exports.runCropRecommendation = (req, res) => {
  const { last_crop, month, season } = req.body;

  const scriptPath = path.join(__dirname, 'rl', 'recommend_crop.py'); // ✅ Corrected path

  const pyProcess = spawn('python', [scriptPath]);

  let output = '';
  let errorOutput = '';

  pyProcess.stdout.on('data', (data) => {
    output += data.toString();
  });

  pyProcess.stderr.on('data', (data) => {
    errorOutput += data.toString();
  });

  pyProcess.stdin.write(`${last_crop}\n`);
  if (month) {
    pyProcess.stdin.write(`${month}\n`);
  } else if (season) {
    pyProcess.stdin.write(`${season}\n`);
  }
  pyProcess.stdin.end();

  pyProcess.on('close', (code) => {
    if (errorOutput) {
      return res.status(500).json({ error: errorOutput });
    }

    try {
      const parsed = JSON.parse(output);
      res.status(200).json(parsed);
    } catch (err) {
      res.status(500).json({ error: 'Invalid response from Python script', raw: output });
    }
  });
};
