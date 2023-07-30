document.addEventListener("DOMContentLoaded", () => {
  const canvas = document.getElementById("gameCanvas");
  const ctx = canvas.getContext("2d");

  let mouseX = canvas.width / 2;
  let mouseY = canvas.height / 2;
  const redDotSize = 30;

  const enemies = []; // enemyの配列

  for (let i = 0; i < 2; i++) {
    enemies.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      size: 40,
      speed: i === 0 ? 3 : 7, // ふたつのenemyの移動速度を異なる値にする
    });
  }

  let isGameOver = false;

  function drawRedDot() {
    ctx.font = `${redDotSize}px FontAwesome`;
    ctx.fillStyle = "red";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText("\uf113", mouseX, mouseY); // ここで赤い円をFontAwesomeのアイコンに変更
  }

  function drawEnemy() {
    ctx.font = `${enemies[0].size}px FontAwesome`;
    ctx.fillStyle = "blue";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText("\uf188", enemies[0].x, enemies[0].y);

    ctx.font = `${enemies[1].size}px FontAwesome`;
    ctx.fillText("\uf188", enemies[1].x, enemies[1].y);
  }

  function drawGameOverMessage() {
    ctx.font = "30px Arial";
    ctx.fillStyle = "red";
    ctx.textAlign = "center";
    ctx.fillText("Game Over", canvas.width / 2, canvas.height / 2);

    ctx.font = "20px Arial";
    ctx.fillStyle = "black";
    ctx.fillText("Click to restart", canvas.width / 2, canvas.height / 2 + 40);
  }

  function checkCollision() {
    for (const enemy of enemies) {
      const dx = mouseX - enemy.x;
      const dy = mouseY - enemy.y;
      const distance = Math.sqrt(dx * dx + dy * dy);

      if (distance < enemy.size + redDotSize) {
        isGameOver = true;
        break; // 衝突が1つでもあればゲームオーバーとする
      }
    }
  }

  function updateGame() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (!isGameOver) {
      drawRedDot();
      drawEnemy();
      moveEnemies();
      checkCollision();
      requestAnimationFrame(updateGame);
    } else {
      drawGameOverMessage();
    }
  }

  function moveEnemies() {
    for (const enemy of enemies) {
      const dx = mouseX - enemy.x;
      const dy = mouseY - enemy.y;
      const distance = Math.sqrt(dx * dx + dy * dy);

      if (distance > enemy.size + redDotSize) {
        enemy.x += (dx / distance) * enemy.speed;
        enemy.y += (dy / distance) * enemy.speed;
      }
    }
  }

  function restartGame() {
    isGameOver = false;
    mouseX = canvas.width / 2;
    mouseY = canvas.height / 2;
    for (const enemy of enemies) {
      enemy.x = Math.random() * canvas.width;
      enemy.y = Math.random() * canvas.height;
    }
    updateGame();
  }

  canvas.addEventListener("mousemove", (event) => {
    const rect = canvas.getBoundingClientRect();
    mouseX = event.clientX - rect.left;
    mouseY = event.clientY - rect.top;
  });

  canvas.addEventListener("click", () => {
    if (isGameOver) {
      restartGame();
    }
  });

  updateGame();
});
