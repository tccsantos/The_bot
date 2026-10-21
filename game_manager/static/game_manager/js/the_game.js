document.addEventListener("DOMContentLoaded", function () {
  const source = document.getElementById("theme-source");

  const allThemes = Array.from(source.querySelectorAll("li"))
    .map(item => ({
      id: item.dataset.id,
      name: item.textContent.trim()
    }))
    .filter(theme => theme.name.length > 0);

  const setup = document.getElementById("setup");
  const tournament = document.getElementById("tournament");
  const startButton = document.getElementById("start-game");
  const playButton = document.getElementById("play-round");
  const restartButton = document.getElementById("restart-game");
  const roundCountInput = document.getElementById("round-count");
  const setupError = document.getElementById("setup-error");

  const roundTitle = document.getElementById("round-title");
  const roundStatus = document.getElementById("round-status");
  const competitorCount = document.getElementById("competitor-count");
  const resultsPanel = document.getElementById("round-results");
  const scoreboard = document.getElementById("scoreboard");
  const roundActions = document.getElementById("round-actions");
  const winnerPanel = document.getElementById("winner-panel");
  const winnerName = document.getElementById("winner-name");
  const winnerDescription = document.getElementById("winner-description");

  document.getElementById("theme-count").textContent = allThemes.length;

  let competitors = [];
  let finalRanking = [];
  let currentRound = 0;
  let maxRounds = 0;

  function shuffle(items) {
    const result = [...items];

    for (let i = result.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [result[i], result[j]] = [result[j], result[i]];
    }

    return result;
  }

  function dispute(competitors) {
    const scores = new Map(
      competitors.map(theme => [theme.id, 0])
    );

    for (const first of competitors) {
      for (const second of competitors) {
        if (first.id === second.id) continue;

        const winner = Math.random() < 0.5 ? first : second;

        scores.set(
          winner.id,
          scores.get(winner.id) + 1
        );
      }
    }

    return competitors
      .map(theme => ({
        id: theme.id,
        name: theme.name,
        score: scores.get(theme.id)
      }))
      .sort((a, b) => b.score - a.score);
  }

  function showRanking(ranking, highestScore = -1) {
    scoreboard.replaceChildren();

    const qualified = Math.ceil(ranking.length / 2);

    ranking.forEach((player, index) => {
      const row = document.createElement("tr");
      const position = document.createElement("td");
      const name = document.createElement("td");
      const score = document.createElement("td");

      position.textContent = index + 1;
      name.textContent = player.name;
      score.textContent = player.score;
      score.className = "text-right font-weight-bold";

      if (index === 0) {
        name.className = "font-weight-bold";
      }
      if (highestScore === -1) {
        if (index < qualified) {
          row.classList.add("table-success");
        }
        else {
          row.classList.add("table-danger");
        }
      }
      else {
        if (player.score === highestScore) {
          row.classList.add("table-success");
        }
        else {
          row.classList.add("table-danger");
        }
      }

      row.append(position, name, score);
      scoreboard.appendChild(row);
    });

    resultsPanel.classList.remove("d-none");
  }

  function showRound() {
    roundTitle.textContent = `Rodada ${currentRound} de ${maxRounds}`;
    competitorCount.textContent =
      `${competitors.length} competidor${competitors.length !== 1 ? "es" : ""}`;

    roundStatus.textContent =
      "Os competidores estão prontos. Inicie a rodada para calcular os resultados.";

    resultsPanel.classList.add("d-none");
    roundActions.classList.remove("d-none");
    playButton.disabled = false;
    playButton.textContent = "Jogar rodada";
  }

  function finishTournament(ranking) {
    finalRanking = ranking;

    const highestScore = ranking[0].score;
    const finalists = ranking.filter(
      player => player.score === highestScore
    );

    const winner = finalists[
      Math.floor(Math.random() * finalists.length)
    ];

    document.getElementById("winner-theme").value = winner.id;

    roundActions.classList.add("d-none");
    winnerPanel.classList.remove("d-none");

    winnerName.textContent = winner.name;

    if (finalists.length > 1) {
      const names = finalists.map(player => player.name);
      winnerDescription.textContent =
        `Houve empate com ${highestScore} pontos entre ` +
        `${names.slice(0, -1).join(", ")}` +
        ` e ` + 
        ` ${names.at(-1)}. ` +
        `O vencedor foi sorteado entre os empatados.`;
    } else {
      winnerDescription.textContent =
        `Vencedor com ${winner.score} pontos na rodada final.`;
    }

    roundStatus.textContent = "Torneio encerrado!";
    roundStatus.className = "alert alert-success";

    showRanking(ranking, highestScore);
  }

  function playRound() {
    playButton.disabled = true;

    currentRound++;

    roundTitle.textContent = `Rodada ${currentRound} de ${maxRounds}`;
    roundStatus.textContent = "Calculando as disputas...";

    const ranking = dispute(competitors);

    showRanking(ranking);

    if (ranking.length < 3 || currentRound >= maxRounds) {
      finishTournament(ranking);
      return;
    }

    const nextCount = Math.ceil(ranking.length / 2);

    competitors = ranking
      .slice(0, nextCount)
      .map(player => ({
        id: player.id,
        name: player.name
      }));

    roundStatus.textContent =
      `${nextCount} competidores avançaram para a próxima rodada.`;

    playButton.textContent = "Avançar para a próxima rodada";
    playButton.disabled = false;
    playButton.onclick = playRound;
  }

  startButton.addEventListener("click", function () {
    setupError.classList.add("d-none");

    if (allThemes.length === 0) {
      setupError.textContent =
        "Não existem temas disponíveis para esta configuração.";
      setupError.classList.remove("d-none");
      return;
    }

    const rounds = Number(roundCountInput.value);

    if (!Number.isInteger(rounds) || rounds < 1 || rounds > 20) {
      setupError.textContent =
        "Informe um número de rodadas entre 1 e 20.";
      setupError.classList.remove("d-none");
      return;
    }

    maxRounds = rounds;
    currentRound = 0;
    competitors = shuffle(allThemes);

    setup.classList.add("d-none");
    tournament.classList.remove("d-none");
    winnerPanel.classList.add("d-none");
    roundStatus.className = "alert alert-info";

    showRound();
    playButton.onclick = playRound;
  });

  restartButton.addEventListener("click", function () {
    tournament.classList.add("d-none");
    setup.classList.remove("d-none");

    competitors = [];
    finalRanking = [];
    currentRound = 0;

    setupError.classList.add("d-none");
    winnerPanel.classList.add("d-none");
    resultsPanel.classList.add("d-none");
    roundActions.classList.remove("d-none");
    roundStatus.className = "alert alert-info";
  });
});