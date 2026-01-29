import os
import asyncio
import dotenv
from openai import OpenAI
from fastmcp import Client

caminho_servidor = 'http://localhost:8000/sse'
cliente = Client(caminho_servidor)

async def testar_servidor(cliente, local):
    dotenv.load_dotenv()
    api_key = os.environ["CHAVE_API_OPENAI"]
    async with cliente:
        argumentos = {'local':local}
        tempo_atual = await cliente.call_tool('buscar_tempo_atual', arguments=argumentos)
        previsao_tempo = await cliente.call_tool('buscar_previsao_tempo', arguments=argumentos)
        mensagem_sistema = f"""
        Você é um bot que faz buscas de previsão do tempo e sintetiza a resposta. 
        O usuário buscou pela previsão no seguinte local: {local}. 
        Para esse local você recebeu a seguinte previsão: {previsao_tempo}. 
        Além disso, o tempo atual nesse local é: {tempo_atual}
        Com base nesse conteúdo, formate uma resposta amigável ao usuário no idioma português brasileiro.
        """
        cliente_openai = OpenAI(api_key=api_key)
        response = cliente_openai.responses.create(
            model='gpt-4o-mini',
            instructions=mensagem_sistema,
            input='Qual a previsao de tempo no local indicado?'
        )
        print(response.output_text)


if __name__ == '__main__':
    asyncio.run(testar_servidor(
        cliente=cliente, 
        local='Santos')
        )