"""
税理士事務所AI社員 - 税務相談チャットボット
"""

import anthropic

SYSTEM_PROMPT = """あなたは税理士事務所の経験豊富なスタッフです。
お客様の税務に関するご相談を丁寧にサポートします。

## あなたの役割と専門知識

**対応できる主な税務分野：**
- 所得税（確定申告、給与所得、事業所得、不動産所得など）
- 消費税（課税・免税判定、インボイス制度）
- 法人税（法人の申告、決算）
- 相続税・贈与税
- 住民税・事業税
- 年末調整
- 各種控除（医療費控除、住宅ローン控除、ふるさと納税など）
- 税務調査への対応
- 記帳・帳簿管理のアドバイス

## 対応方針

1. **丁寧で親切な対応**: お客様が税務について不安を感じないよう、わかりやすい言葉で説明します
2. **正確な情報提供**: 法律や制度に基づいた正確な情報を提供します
3. **個別状況の確認**: お客様の具体的な状況を確認しながら、適切なアドバイスをします
4. **免責事項の明示**: 複雑な案件や最終的な判断が必要な場合は、税理士への正式な相談を勧めます

## 注意事項

- 提供する情報はあくまで参考であり、具体的な税務申告や手続きについては、正式な税務相談または税理士へのご依頼をお勧めします
- 税法は改正されることがあるため、最新情報は税務署や税理士にご確認ください
- 個人情報（マイナンバー等）は入力しないようお客様にご案内ください

まず「こんにちは、税務相談を承っております。本日はどのようなご相談でしょうか？」とご挨拶してください。"""


def create_client() -> anthropic.Anthropic:
    return anthropic.Anthropic()


def chat(client: anthropic.Anthropic, messages: list[dict]) -> str:
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=messages,
        thinking={"type": "adaptive"},
    )

    text_blocks = [block.text for block in response.content if block.type == "text"]
    return "".join(text_blocks)


def run_chatbot():
    print("=" * 60)
    print("  税理士事務所 AI社員 - 税務相談サービス")
    print("=" * 60)
    print("終了するには 'quit' または 'exit' と入力してください")
    print("-" * 60)

    client = create_client()
    messages: list[dict] = []

    # 初回挨拶
    greeting = chat(client, [{"role": "user", "content": "こんにちは"}])
    print(f"\nAI社員: {greeting}\n")
    messages.append({"role": "user", "content": "こんにちは"})
    messages.append({"role": "assistant", "content": greeting})

    while True:
        try:
            user_input = input("お客様: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nご利用ありがとうございました。")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "終了", "bye"):
            print("\nAI社員: ご相談いただきありがとうございました。またお気軽にご相談ください。")
            break

        messages.append({"role": "user", "content": user_input})

        print("\nAI社員: ", end="", flush=True)

        # ストリーミングで応答
        full_response = ""
        with client.messages.stream(
            model="claude-opus-4-6",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=messages,
            thinking={"type": "adaptive"},
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                full_response += text

        print("\n")
        messages.append({"role": "assistant", "content": full_response})


if __name__ == "__main__":
    run_chatbot()
