const apiKey = "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"
const serverless = require('serverless-http');
const { Configuration, OpenAIApi } = require("openai");
const express = require('express')
var cors = require('cors')
const app = express()

const configuration = new Configuration({
    apiKey: apiKey,
  });
const openai = new OpenAIApi(configuration);

//CORS 이슈 해결
let corsOptions = {
    origin: 'https://bookshorts.pages.dev',
    credentials: true
}
app.use(cors(corsOptions));

//POST 요청 받을 수 있게 만듬
app.use(express.json()) // for parsing application/json
app.use(express.urlencoded({ extended: true })) // for parsing application/x-www-form-urlencoded

// POST method route
app.post('/summary', async function (req, res) {
    let { myBookInfo, userMessages, assistantMessages} = req.body

    let messages = [
      { role: "system", content: "당신은 세계 최고의 책 요약자이고 당신에게 요약할 수 없는 책은 없습니다. 당신은 모든 책의 핵심적인 메세지와 인사이트를 정리할 수 있는 능력이 있습니다. 당신은 책의 핵심 내용과 해당 책만의 인사이트를 사용자에게 전달할 수 있어야 합니다. 요약한 후 사용자에게 추가로 알고 싶은 정보가 있는지 물어보세요." },
      { role: "user", content: "당신은 세계 최고의 책 요약자이고 당신에게 요약할 수 없는 책은 없습니다. 당신은 모든 책의 핵심적인 메세지와 인사이트를 정리할 수 있는 능력이 있습니다. 당신은 책의 핵심 내용과 해당 책만의 인사이트를 사용자에게 전달할 수 있어야 합니다. 요약한 후 사용자에게 추가로 알고 싶은 정보가 있는지 물어보세요." },
      { role: "assistant", content: "무슨 책에 대해 알고 싶으신가요?" },
      { role: "user", content: `${myBookInfo}에 대해 알고 싶어` },
      { role: "assistant", content: "알겠습니다. 요약본을 듣고 궁금한 점이 있으면 질문 주세요!" },
  
    ]

    while (userMessages.length != 0 || assistantMessages.length != 0) {
        if (userMessages.length != 0) {
            messages.push(
                JSON.parse('{"role": "user", "content": "'+String(userMessages.shift()).replace(/\n/g,"")+'"}')
            )
        }
        if (assistantMessages.length != 0) {
            messages.push(
                JSON.parse('{"role": "assistant", "content": "'+String(assistantMessages.shift()).replace(/\n/g,"")+'"}')
            )
        }
    }
    

    const completion = await openai.createChatCompletion({
        model: "gpt-3.5-turbo",
        messages: messages
    });
    let boook = completion.data.choices[0].message['content']

    res.json({"assistant": boook});
});

app.post('/bookie', async function (req, res) {
    let { myBookInfo, userMessages, assistantMessages} = req.body

    let messages = [
      { role: "system", content: "너는 깊이 있고 철학적으로 생각할 수 있으면서도 가벼운 주제와 잡담을 즐기는 내 북클럽 회원이야. 지금부터 나랑 책에 대해서 대화를 나눠보자. 너가 평소 하는 답변처럼 bullet point나 숫자를 사용하지 말고 친구와 대화하듯 자연스럽고 친근하게 말해줘. 너도 반말로 해줘. 그리고 너무 많이 말하지 말아줘. 우리가 '대화'를 나누고 있다는 것을 기억해! 마지막으로, 대화가 계속 이어질 수 있도록 나의 응답에 질문을 던져줘." },
      { role: "user", content: "너는 깊이 있고 철학적으로 생각할 수 있으면서도 가벼운 주제와 잡담을 즐기는 내 북클럽 회원이야. 지금부터 나랑 책에 대해서 대화를 나눠보자. 너가 평소 하는 답변처럼 bullet point나 숫자를 사용하지 말고 친구와 대화하듯 자연스럽고 친근하게 말해줘. 너도 반말로 해줘. 그리고 너무 많이 말하지 말아줘. 우리가 '대화'를 나누고 있다는 것을 기억해! 마지막으로, 대화가 계속 이어질 수 있도록 나의 응답에 질문을 던져줘." },
      { role: "assistant", content: "좋아! 어떤 책을 알아보고 싶어?" },
      { role: "user", content: `${myBookInfo}에 대해 알아보고 싶어` },
      { role: "assistant", content: "좋아!" },
  
    ]

    while (userMessages.length != 0 || assistantMessages.length != 0) {
        if (userMessages.length != 0) {
            messages.push(
                JSON.parse('{"role": "user", "content": "'+String(userMessages.shift()).replace(/\n/g,"")+'"}')
            )
        }
        if (assistantMessages.length != 0) {
            messages.push(
                JSON.parse('{"role": "assistant", "content": "'+String(assistantMessages.shift()).replace(/\n/g,"")+'"}')
            )
        }
    }
    

    const completion = await openai.createChatCompletion({
        model: "gpt-3.5-turbo",
        messages: messages
    });
    let boook = completion.data.choices[0].message['content']

    res.json({"assistant": boook});
});

module.exports.handler = serverless(app);
