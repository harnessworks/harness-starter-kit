(function () {
  "use strict";

  var fallbackLang = "en";
  var storageKey = "hks-language";
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var activeChapter = "problem";
  var terminalSignature = "";
  var terminalRunId = 0;

  var commandText = [
    "Read ./harness-starter-kit first, then apply the harness engineering starter kit to this repository.",
    "",
    "Treat the current working directory as the target repository. Treat ./harness-starter-kit as read-only reference material unless I explicitly ask you to edit the kit itself.",
    "",
    "Preserve this repository's existing architecture, tools, package manager, commands, and conventions. Add only the minimum missing harness files. Prefer updating existing docs/configs over duplicating them. Do not overwrite or delete existing files without explaining why.",
    "",
    "Finish with a short adoption report listing files changed, checks I can run, assumptions made, and remaining manual steps."
  ].join("\n");

  var copy = {
    en: {
      hero: {
        eyebrow: "DOS MODE / REPO HARNESS ONLINE",
        title: "Make agent context survive the session.",
        lede:
          "harness-starter-kit turns repeated coding-agent instructions into durable repo artifacts: rules, checks, feedback loops, and memory.",
        primaryCta: "Copy agent prompt",
        secondaryCta: "Watch the boot log",
        scrollCue: "Scroll to inspect"
      },
      chapters: {
        problem: {
          eyebrow: "01 / The failure mode",
          title: "Prompts vanish. Repos remember nothing by default.",
          body:
            "A chat instruction can guide one run, but the next agent starts cold unless the repository stores the rule."
        },
        solution: {
          eyebrow: "02 / The harness",
          title: "Move the rule into the project.",
          body:
            "A harness is not another framework. It is the repo-native layer that tells agents what to preserve, what to check, and what history matters."
        },
        components: {
          eyebrow: "03 / The components",
          title: "Instructions, constraints, feedback, memory.",
          body:
            "The kit installs the smallest useful set: AGENTS.md, knowledge folders, profile snippets, and drift checks."
        },
        adoption: {
          eyebrow: "04 / The workflow",
          title: "Inspect first. Install only what is missing.",
          body:
            "The target repository stays the source of truth. Existing tools win over starter-kit defaults."
        },
        quickStart: {
          eyebrow: "05 / The command",
          title: "The quickest path is an agent prompt.",
          body:
            "Download this kit inside the target repository, then ask your coding agent to read it and apply only the missing harness pieces."
        }
      },
      components: {
        eyebrow: "SYSTEM MAP",
        title: "What the starter kit leaves behind",
        instructions: {
          title: "Agent instructions",
          body: "Concise project rules in AGENTS.md so every session begins with the same durable context."
        },
        constraints: {
          title: "Architecture constraints",
          body: "Lint, type, import, and review checks that catch invalid structure before merge."
        },
        feedback: {
          title: "Feedback loops",
          body: "Tests, CI, pre-commit hooks, examples, and clear failures that steer agents quickly."
        },
        knowledge: {
          title: "Knowledge store",
          body: "Decisions, failures, conventions, and domain language captured under docs/."
        }
      },
      structure: {
        eyebrow: "DIRECTORY TREE",
        title: "See the harness before it lands.",
        body:
          "The starter kit sits inside the target repository while the agent reads it, then installs only the missing durable pieces into the target root.",
        kitLabel: "Starter kit",
        targetLabel: "Target repo after adoption"
      },
      quick: {
        eyebrow: "QUICK START",
        title: "Ask an agent to apply the kit.",
        body:
          "Clone or download harness-starter-kit inside a target repository. From the target repo, give your coding agent this prompt.",
        copy: "Copy agent prompt",
        copied: "Prompt copied.",
        selected: "Prompt selected. Press Ctrl+C to copy.",
        copyFailed: "Copy unavailable. Select the prompt manually."
      },
      final: {
        eyebrow: "END SESSION / KEEP THE CONTEXT",
        cta: "Get started",
        github: "View on GitHub"
      },
      footer: {
        tagline: "Durable context for coding agents."
      },
      terminal: {
        problem: {
          command: "explain problem",
          lines: [
            "You tell an agent a rule in chat.",
            "That rule helps only this session.",
            "The next agent starts without that memory.",
            "So repeated mistakes come back."
          ]
        },
        solution: {
          command: "explain harness",
          lines: [
            "Put harness-starter-kit inside target-repo.",
            "Ask the agent to read ./harness-starter-kit.",
            "The agent inspects the project first.",
            "Then it adds only the missing harness pieces."
          ]
        },
        components: {
          command: "explain files",
          lines: [
            "AGENTS.md tells future agents the rules.",
            "docs/ stores decisions, failures, and terms.",
            "scripts/check_* catches stale docs or drift.",
            "profiles/ gives optional Python and TS snippets."
          ]
        },
        adoption: {
          command: "explain adoption",
          lines: [
            "1. Read the target README, tools, and CI.",
            "2. Keep the target repo as the source of truth.",
            "3. Avoid overwriting existing files.",
            "4. Finish with an adoption report."
          ]
        },
        quickStart: {
          command: "explain quick-start",
          lines: [
            "Copy the agent prompt below.",
            "Open target-repo with your coding agent.",
            "Paste: Read ./harness-starter-kit first.",
            "Review the report before merging changes."
          ]
        }
      }
    },
    ko: {
      hero: {
        eyebrow: "DOS MODE / REPO HARNESS ONLINE",
        title: "에이전트 컨텍스트를 세션 밖에 남기세요.",
        lede:
          "harness-starter-kit은 반복되는 코딩 에이전트 지시를 규칙, 검사, 피드백 루프, 기억으로 저장소 안에 남깁니다.",
        primaryCta: "에이전트 프롬프트 복사",
        secondaryCta: "부트 로그 보기",
        scrollCue: "스크롤해서 확인"
      },
      chapters: {
        problem: {
          eyebrow: "01 / 실패 모드",
          title: "프롬프트는 사라지고, 저장소는 기본적으로 기억하지 않습니다.",
          body:
            "채팅 지시는 한 번의 실행을 도울 수 있지만, 규칙이 저장소에 남지 않으면 다음 에이전트는 다시 처음부터 시작합니다."
        },
        solution: {
          eyebrow: "02 / 하네스",
          title: "규칙을 프로젝트 안으로 옮깁니다.",
          body:
            "하네스는 또 다른 프레임워크가 아닙니다. 에이전트가 무엇을 보존하고, 무엇을 검사하고, 어떤 이력을 기억해야 하는지 알려주는 저장소 기반 계층입니다."
        },
        components: {
          eyebrow: "03 / 구성 요소",
          title: "지침, 제약, 피드백, 기억.",
          body:
            "이 키트는 AGENTS.md, 지식 폴더, 프로필 스니펫, drift check로 가장 작은 실용 세트를 설치합니다."
        },
        adoption: {
          eyebrow: "04 / 적용 흐름",
          title: "먼저 살피고, 없는 것만 설치합니다.",
          body:
            "대상 저장소가 항상 기준입니다. 기존 도구가 있다면 starter-kit 기본값보다 우선합니다."
        },
        quickStart: {
          eyebrow: "05 / 명령",
          title: "가장 빠른 시작은 에이전트 프롬프트입니다.",
          body:
            "이 키트를 대상 저장소 안에 내려받고, 코딩 에이전트에게 읽은 뒤 누락된 harness 조각만 적용하라고 요청합니다."
        }
      },
      components: {
        eyebrow: "SYSTEM MAP",
        title: "스타터 키트가 저장소에 남기는 것",
        instructions: {
          title: "에이전트 지침",
          body: "모든 세션이 같은 durable context에서 시작하도록 AGENTS.md에 간결한 프로젝트 규칙을 둡니다."
        },
        constraints: {
          title: "아키텍처 제약",
          body: "lint, type, import, review check로 잘못된 구조가 merge되기 전에 잡히게 합니다."
        },
        feedback: {
          title: "피드백 루프",
          body: "test, CI, pre-commit hook, 예제, 명확한 실패 메시지로 에이전트를 빠르게 교정합니다."
        },
        knowledge: {
          title: "지식 저장소",
          body: "결정, 실패, 컨벤션, 도메인 언어를 docs/ 아래에 저장합니다."
        }
      },
      structure: {
        eyebrow: "DIRECTORY TREE",
        title: "적용 전에 폴더 구조를 확인하세요.",
        body:
          "스타터 키트는 대상 저장소 안에 둡니다. 에이전트가 키트를 읽고, 대상 저장소 루트에는 누락된 durable 조각만 설치합니다.",
        kitLabel: "스타터 키트",
        targetLabel: "적용 후 대상 저장소"
      },
      quick: {
        eyebrow: "빠른 시작",
        title: "에이전트에게 키트 적용을 요청합니다.",
        body:
          "harness-starter-kit을 대상 저장소 안에 클론하거나 다운로드하세요. 대상 저장소에서 코딩 에이전트에게 이 프롬프트를 주세요.",
        copy: "에이전트 프롬프트 복사",
        copied: "프롬프트를 복사했습니다.",
        selected: "프롬프트를 선택했습니다. Ctrl+C로 복사하세요.",
        copyFailed: "복사를 사용할 수 없습니다. 프롬프트를 직접 선택하세요."
      },
      final: {
        eyebrow: "END SESSION / KEEP THE CONTEXT",
        cta: "시작하기",
        github: "GitHub로 이동"
      },
      footer: {
        tagline: "코딩 에이전트를 위한 durable context."
      },
      terminal: {
        problem: {
          command: "explain problem",
          lines: [
            "채팅에서 에이전트에게 규칙을 알려줍니다.",
            "그 규칙은 이번 세션에서만 도움이 됩니다.",
            "다음 에이전트는 그 기억 없이 시작합니다.",
            "그래서 같은 실수가 다시 돌아옵니다."
          ]
        },
        solution: {
          command: "explain harness",
          lines: [
            "target-repo 안에 harness-starter-kit을 둡니다.",
            "에이전트에게 ./harness-starter-kit을 읽게 합니다.",
            "에이전트는 먼저 프로젝트를 살핍니다.",
            "그 다음 누락된 harness 조각만 추가합니다."
          ]
        },
        components: {
          command: "explain files",
          lines: [
            "AGENTS.md는 다음 에이전트에게 규칙을 알려줍니다.",
            "docs/는 결정, 실패, 용어를 저장합니다.",
            "scripts/check_*는 문서와 구조 drift를 잡습니다.",
            "profiles/는 Python과 TS용 참고 스니펫입니다."
          ]
        },
        adoption: {
          command: "explain adoption",
          lines: [
            "1. 대상 README, 도구, CI를 먼저 읽습니다.",
            "2. 대상 저장소를 기준으로 삼습니다.",
            "3. 기존 파일은 함부로 덮어쓰지 않습니다.",
            "4. 마지막에 적용 보고서를 남깁니다."
          ]
        },
        quickStart: {
          command: "explain quick-start",
          lines: [
            "아래 에이전트 프롬프트를 복사합니다.",
            "target-repo를 코딩 에이전트로 엽니다.",
            "붙여넣기: ./harness-starter-kit을 먼저 읽어줘.",
            "merge 전 적용 보고서를 확인합니다."
          ]
        }
      }
    },
    ja: {
      hero: {
        eyebrow: "DOS MODE / REPO HARNESS ONLINE",
        title: "エージェントの文脈をセッションの外へ残す。",
        lede:
          "harness-starter-kit は、繰り返し使うコーディングエージェントへの指示を、ルール、チェック、フィードバックループ、記憶としてリポジトリに残します。",
        primaryCta: "エージェントプロンプトをコピー",
        secondaryCta: "ブートログを見る",
        scrollCue: "スクロールして確認"
      },
      chapters: {
        problem: {
          eyebrow: "01 / 失敗モード",
          title: "プロンプトは消え、リポジトリは標準では記憶しません。",
          body:
            "チャットの指示は一度の実行を助けますが、ルールがリポジトリに残らなければ次のエージェントはまたゼロから始めます。"
        },
        solution: {
          eyebrow: "02 / harness",
          title: "ルールをプロジェクトへ移します。",
          body:
            "harness は別のフレームワークではありません。何を保ち、何を確認し、どの履歴を大事にするかをエージェントへ伝える repo-native な層です。"
        },
        components: {
          eyebrow: "03 / 構成要素",
          title: "指示、制約、フィードバック、記憶。",
          body:
            "このキットは AGENTS.md、知識フォルダ、プロファイル用スニペット、drift check という最小限で実用的なセットを導入します。"
        },
        adoption: {
          eyebrow: "04 / 導入フロー",
          title: "まず調べ、足りないものだけを入れます。",
          body:
            "対象リポジトリが常に正です。既存ツールがある場合は starter-kit の既定値より優先します。"
        },
        quickStart: {
          eyebrow: "05 / コマンド",
          title: "最短の開始方法はエージェントプロンプトです。",
          body:
            "このキットを対象リポジトリの中に置き、コーディングエージェントに読ませて不足している harness だけを適用させます。"
        }
      },
      components: {
        eyebrow: "SYSTEM MAP",
        title: "スターターキットがリポジトリに残すもの",
        instructions: {
          title: "エージェント指示",
          body: "すべてのセッションが同じ durable context で始まるように、AGENTS.md に簡潔なプロジェクトルールを置きます。"
        },
        constraints: {
          title: "アーキテクチャ制約",
          body: "lint、type、import、review check により、不正な構造を merge 前に検出します。"
        },
        feedback: {
          title: "フィードバックループ",
          body: "test、CI、pre-commit hook、例、明確な失敗メッセージでエージェントを素早く修正します。"
        },
        knowledge: {
          title: "ナレッジストア",
          body: "decision、failure、convention、domain language を docs/ 配下に保存します。"
        }
      },
      structure: {
        eyebrow: "DIRECTORY TREE",
        title: "導入前にフォルダ構成を確認できます。",
        body:
          "スターターキットは対象リポジトリの中に置きます。エージェントがそれを読み、対象リポジトリのルートには不足している durable な要素だけを導入します。",
        kitLabel: "スターターキット",
        targetLabel: "導入後の対象リポジトリ"
      },
      quick: {
        eyebrow: "クイックスタート",
        title: "エージェントにキットの適用を依頼します。",
        body:
          "harness-starter-kit を対象リポジトリの中にクローンまたはダウンロードします。対象リポジトリで、このプロンプトをコーディングエージェントに渡してください。",
        copy: "エージェントプロンプトをコピー",
        copied: "プロンプトをコピーしました。",
        selected: "プロンプトを選択しました。Ctrl+C でコピーしてください。",
        copyFailed: "コピーできません。プロンプトを手動で選択してください。"
      },
      final: {
        eyebrow: "END SESSION / KEEP THE CONTEXT",
        cta: "はじめる",
        github: "GitHub を見る"
      },
      footer: {
        tagline: "コーディングエージェントのための durable context."
      },
      terminal: {
        problem: {
          command: "explain problem",
          lines: [
            "チャットでエージェントにルールを伝えます。",
            "そのルールは今回のセッションだけを助けます。",
            "次のエージェントはその記憶なしで始まります。",
            "そのため同じミスが戻ってきます。"
          ]
        },
        solution: {
          command: "explain harness",
          lines: [
            "target-repo の中に harness-starter-kit を置きます。",
            "エージェントに ./harness-starter-kit を読ませます。",
            "エージェントはまずプロジェクトを調べます。",
            "その後、不足している harness だけを追加します。"
          ]
        },
        components: {
          command: "explain files",
          lines: [
            "AGENTS.md は次のエージェントへルールを伝えます。",
            "docs/ は decision、failure、用語を保存します。",
            "scripts/check_* は文書や構造の drift を検出します。",
            "profiles/ は Python と TS の参考スニペットです。"
          ]
        },
        adoption: {
          command: "explain adoption",
          lines: [
            "1. 対象 README、ツール、CI を先に読みます。",
            "2. 対象リポジトリを正とします。",
            "3. 既存ファイルを勝手に上書きしません。",
            "4. 最後に導入レポートを残します。"
          ]
        },
        quickStart: {
          command: "explain quick-start",
          lines: [
            "下のエージェントプロンプトをコピーします。",
            "target-repo をコーディングエージェントで開きます。",
            "貼り付け: まず ./harness-starter-kit を読んでください。",
            "merge 前に導入レポートを確認します。"
          ]
        }
      }
    },
    "zh-CN": {
      hero: {
        eyebrow: "DOS MODE / REPO HARNESS ONLINE",
        title: "让代理上下文留在会话之外。",
        lede:
          "harness-starter-kit 会把重复的代码代理指令变成仓库里的规则、检查、反馈回路和记忆。",
        primaryCta: "复制代理提示词",
        secondaryCta: "查看启动日志",
        scrollCue: "滚动查看"
      },
      chapters: {
        problem: {
          eyebrow: "01 / 失败模式",
          title: "提示词会消失，仓库默认不会记住上下文。",
          body:
            "聊天指令可以指导一次运行，但如果规则没有进入仓库，下一个代理仍然会从冷启动开始。"
        },
        solution: {
          eyebrow: "02 / harness",
          title: "把规则移入项目。",
          body:
            "harness 不是另一个框架。它是 repo-native 的一层，告诉代理要保留什么、检查什么、记住哪些历史。"
        },
        components: {
          eyebrow: "03 / 组成部分",
          title: "指令、约束、反馈、记忆。",
          body:
            "这个套件安装最小但有用的一组内容：AGENTS.md、知识目录、profile 片段和 drift check。"
        },
        adoption: {
          eyebrow: "04 / 采用流程",
          title: "先检查，只安装缺失部分。",
          body:
            "目标仓库始终是事实来源。已有工具优先于 starter-kit 的默认设置。"
        },
        quickStart: {
          eyebrow: "05 / 命令",
          title: "最快的开始方式是代理提示词。",
          body:
            "把这个套件放到目标仓库内部，然后让代码代理阅读它并只应用缺失的 harness 部分。"
        }
      },
      components: {
        eyebrow: "SYSTEM MAP",
        title: "starter kit 会留在仓库中的内容",
        instructions: {
          title: "代理指令",
          body: "把简洁的项目规则写入 AGENTS.md，让每个会话都从同一份 durable context 开始。"
        },
        constraints: {
          title: "架构约束",
          body: "用 lint、type、import 和 review check 在合并前捕获错误结构。"
        },
        feedback: {
          title: "反馈回路",
          body: "用 test、CI、pre-commit hook、示例和清晰错误信息快速校正代理。"
        },
        knowledge: {
          title: "知识库",
          body: "把 decision、failure、convention 和 domain language 保存到 docs/ 下。"
        }
      },
      structure: {
        eyebrow: "DIRECTORY TREE",
        title: "在采用之前先看清目录结构。",
        body:
          "starter kit 放在目标仓库内部。代理先读取它，然后只把缺失的 durable 部分安装到目标仓库根目录中。",
        kitLabel: "starter kit",
        targetLabel: "采用后的目标仓库"
      },
      quick: {
        eyebrow: "快速开始",
        title: "让代理应用这个套件。",
        body:
          "把 harness-starter-kit 克隆或下载到目标仓库内部。然后在目标仓库中，把这个提示词交给代码代理。",
        copy: "复制代理提示词",
        copied: "提示词已复制。",
        selected: "提示词已选中。请按 Ctrl+C 复制。",
        copyFailed: "无法复制。请手动选择提示词。"
      },
      final: {
        eyebrow: "END SESSION / KEEP THE CONTEXT",
        cta: "开始使用",
        github: "查看 GitHub"
      },
      footer: {
        tagline: "面向代码代理的 durable context。"
      },
      terminal: {
        problem: {
          command: "explain problem",
          lines: [
            "你在聊天中告诉代理一条规则。",
            "这条规则只帮助当前会话。",
            "下一个代理不会自动记住它。",
            "所以同样的错误可能再次出现。"
          ]
        },
        solution: {
          command: "explain harness",
          lines: [
            "把 harness-starter-kit 放进 target-repo。",
            "让代理先读取 ./harness-starter-kit。",
            "代理会先检查现有项目。",
            "然后只添加缺失的 harness 部分。"
          ]
        },
        components: {
          command: "explain files",
          lines: [
            "AGENTS.md 把规则告诉之后的代理。",
            "docs/ 保存决策、失败记录和术语。",
            "scripts/check_* 检测文档和结构 drift。",
            "profiles/ 提供 Python 和 TS 参考片段。"
          ]
        },
        adoption: {
          command: "explain adoption",
          lines: [
            "1. 先阅读目标 README、工具和 CI。",
            "2. 以目标仓库为事实来源。",
            "3. 不随意覆盖已有文件。",
            "4. 最后留下采用报告。"
          ]
        },
        quickStart: {
          command: "explain quick-start",
          lines: [
            "复制下面的代理提示词。",
            "用你的代码代理打开 target-repo。",
            "粘贴: 先阅读 ./harness-starter-kit。",
            "合并前检查采用报告。"
          ]
        }
      }
    }
  };

  function getValue(path, lang) {
    var parts = path.split(".");
    var node = copy[lang] || copy[fallbackLang];
    for (var i = 0; i < parts.length; i += 1) {
      if (!node || typeof node !== "object" || !(parts[i] in node)) {
        return getValue(path, fallbackLang);
      }
      node = node[parts[i]];
    }
    return node;
  }

  function typeText(element, text, speed) {
    if (!element) {
      return;
    }
    if (element._typingTimers) {
      element._typingTimers.forEach(function (timer) {
        window.clearTimeout(timer);
      });
    }
    element._typingTimers = [];
    if (reduceMotion) {
      element.textContent = text;
      return;
    }
    element.textContent = "";
    Array.prototype.forEach.call(text, function (character, index) {
      var timer = window.setTimeout(function () {
        element.textContent += character;
      }, index * speed);
      element._typingTimers.push(timer);
    });
  }

  function typeTerminal(text) {
    var output = document.querySelector("#terminal-output code");
    if (!output) {
      return;
    }
    if (reduceMotion) {
      output.textContent = text;
      return;
    }
    terminalRunId += 1;
    var runId = terminalRunId;
    output.textContent = "";
    var index = 0;
    var chunk = 3;
    function tick() {
      if (runId !== terminalRunId) {
        return;
      }
      output.textContent += text.slice(index, index + chunk);
      index += chunk;
      if (index < text.length) {
        window.setTimeout(tick, 12);
      }
    }
    tick();
  }

  function activeLanguage() {
    var saved = window.localStorage.getItem(storageKey);
    return copy[saved] ? saved : fallbackLang;
  }

  function terminalText(lang, chapterName) {
    var script = getValue("terminal." + chapterName, lang);
    var lines = ["C:\\HKS> " + script.command, ""].concat(script.lines);
    return lines.join("\n");
  }

  function updateTerminal(lang, chapterName) {
    var signature = lang + ":" + chapterName;
    if (signature === terminalSignature) {
      return;
    }
    terminalSignature = signature;
    typeTerminal(terminalText(lang, chapterName));
  }

  function setLanguage(lang) {
    var selected = copy[lang] ? lang : fallbackLang;
    window.localStorage.setItem(storageKey, selected);
    document.documentElement.lang = selected;

    document.querySelectorAll("[data-i18n]").forEach(function (node) {
      node.textContent = getValue(node.getAttribute("data-i18n"), selected);
    });

    document.querySelectorAll("[data-lang]").forEach(function (button) {
      button.setAttribute("aria-pressed", String(button.getAttribute("data-lang") === selected));
    });

    typeText(document.querySelector("[data-i18n-type='hero.title']"), getValue("hero.title", selected), 24);
    typeText(document.getElementById("hero-command"), "HARNESS STARTER KIT", 34);
    terminalSignature = "";
    updateTerminal(selected, activeChapter);
  }

  function setupLanguageButtons() {
    document.querySelectorAll("[data-lang]").forEach(function (button) {
      button.addEventListener("click", function () {
        setLanguage(button.getAttribute("data-lang"));
      });
    });
  }

  function setupChapters() {
    var chapters = document.querySelectorAll("[data-chapter]");
    if (!("IntersectionObserver" in window)) {
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) {
            return;
          }
          activeChapter = entry.target.getAttribute("data-chapter");
          chapters.forEach(function (chapter) {
            chapter.classList.toggle("is-active", chapter === entry.target);
          });
          updateTerminal(activeLanguage(), activeChapter);
        });
      },
      {
        root: null,
        threshold: 0.58
      }
    );

    chapters.forEach(function (chapter) {
      observer.observe(chapter);
    });
  }

  function setupParallax() {
    if (reduceMotion) {
      return;
    }
    var ticking = false;
    function update() {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      var progress = max > 0 ? window.scrollY / max : 0;
      document.documentElement.style.setProperty("--scroll-progress", progress.toFixed(4));

      var stage = document.querySelector(".terminal-stage");
      if (stage) {
        var stageBox = stage.getBoundingClientRect();
        var centerOffset = (stageBox.top + stageBox.height / 2 - window.innerHeight / 2) / window.innerHeight;
        stage.style.setProperty("--stage-y", String(Math.round(centerOffset * -20)));
      }
      ticking = false;
    }

    function requestUpdate() {
      if (!ticking) {
        window.requestAnimationFrame(update);
        ticking = true;
      }
    }

    window.addEventListener("scroll", requestUpdate, { passive: true });
    window.addEventListener("resize", requestUpdate);
    requestUpdate();
  }

  function setupCopyButton() {
    var button = document.querySelector(".copy-button");
    var status = document.getElementById("copy-status");
    if (!button || !status) {
      return;
    }

    function legacyCopy() {
      var command = document.getElementById("quick-command");
      if (!command || !document.createRange || !window.getSelection) {
        return "failed";
      }
      var range = document.createRange();
      range.selectNodeContents(command);
      var selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      try {
        return document.execCommand("copy") ? "copied" : "selected";
      } catch (error) {
        return "selected";
      }
    }

    button.addEventListener("click", function () {
      var lang = activeLanguage();
      if (!navigator.clipboard || !navigator.clipboard.writeText) {
        var fallbackResult = legacyCopy();
        status.textContent =
          fallbackResult === "copied"
            ? getValue("quick.copied", lang)
            : fallbackResult === "selected"
              ? getValue("quick.selected", lang)
              : getValue("quick.copyFailed", lang);
        return;
      }
      navigator.clipboard
        .writeText(commandText)
        .then(function () {
          status.textContent = getValue("quick.copied", lang);
        })
        .catch(function () {
          var fallbackResult = legacyCopy();
          status.textContent =
            fallbackResult === "copied"
              ? getValue("quick.copied", lang)
              : fallbackResult === "selected"
                ? getValue("quick.selected", lang)
                : getValue("quick.copyFailed", lang);
        });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    setupLanguageButtons();
    setupChapters();
    setupParallax();
    setupCopyButton();
    setLanguage(activeLanguage());
  });
})();
