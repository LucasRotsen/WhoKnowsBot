# WhoKnowsBot


## Overview do projeto
WhoKnowsBot é um robô social. Ele  foi desenvolvido como um estudo de caso sobre desenvolvimento de componentes de software associados a computação por humanos (human computation). O estudo é parte do projeto PIBIC-CNPq coordenado pelo prof. Lesandro Ponciano e conduzido pelo aluno bolsista Arthur Vinicius Soares, no curso Bacharelado em Sistemas de Informação da Pontifícia Universidade Católica de Minas Gerais (PUC Minas). O projeto foi executado entre Agosto de 2017 e Julho de 2018.

De forma geral, o robô possui três funcionalidades principais que podem ser acionadas pelo usuário: atribuição, agregação e contagem de termos. Pela funcionalidade de atribuição (escalonamento), o usuário informa ao robô um tópico e o robô responde ao usuário quem (entre as pessoa que seguem o usuário no twitter) mais fala sobre aquele tópico no twitter. Pela funcionalidade de agregação, o usuário informa ao robô um tópico e o robô responde ao usuário quantas (entre as pessoa o usuário segue no twitter) falaram sobre aquele tópico no twitter. Pela contagem de termos o robô enumera os termos mais frequentes na timeline do usuário e o responde com uma nuvem de palavras.

Há uma instância do robô ativa em https://twitter.com/whoknowsbot. Informações sobre como conversar com o robô e explicações sobre as respostas dele estão em https://drive.google.com/file/d/1jhFCTByFLM2uOGsqa_BUB0BR9FarKnlV/view.

Abaixo estão mais informações sobre a implementação do robô.


## Configuração inicial
As configurações do robô são acessadas através da pasta _configurarion_ localizada na raiz do projeto.

No arquivo _twitter_connection.py_ é necessário atribuir valores às variáveis:

    - consumerKey
    - consumerSecret
    - accessToken
    - accessTokenSecret

Essas informações estão disponíveis na [página do desenvolvedor](https://apps.twitter.com) do Twitter:

    consumerKey = 'XXXXXXXXXXXXXXXXXXXXXXXXX'
    consumerSecret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    accessToken = '0000000000-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    accessTokenSecret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

No arquivo _bot_config.py_ é possível parametrizar se o robô deve imprimir no console os passos de sua execução, por padrão este valor é **True**:

    - verbose

Ainda no arquivo _bot_config.py_ existem dois parâmetros que influenciam no comportamento da funcionalidade de contagem de termos:

    - amount_of_terms_to_retrieve
    - should_count_mentions

O parâmetro _amount_of_terms_to_retrieve_ define a quantidade de termos que serão retornados pelo método _most_used_terms_. Por padrão este valor é **10**.

O parâmetro _should_count_mentions_ especifica se o método _most_used_terms_ deve contar menções. Por padrão este valor é **False**. 

Exemplo: No tweet "@dan_abramov I love react" os termos "love" e "react" seriam contados uma vez cada e os termos "I" e "@dan_abramov" seriam ignorados. Caso `should_count_mentions = True`, o termo "@dan_abramov" também seria contado.


## Executando o Robô
_Este projeto foi testado no sistema operacional Ubuntu 16.04 com Python 3.5.2._ 

Para executar o robô é necessário checar se o `pip` está instalado com o comando `pip --version`. Se o comando não for reconhecido é possível instalá-lo no Ubuntu 16.04 com o gerenciador de pacotes:

     # apt-get update
     # apt-get install python-pip

Em seguida verifique se o `pipenv` está instalado com o comando `pipenv --version`. Caso o comando não seja reconhecido é possível instalá-lo com o pip:

     $ pip install --user pipenv

Com o pipenv instalado, execute na pasta raiz do projeto para instalar as dependências:

     $ pipenv install

Para iniciar o robô:

     $ pipenv run python main.py

Para acessar as funcionalidades do robô sem a interação pelo Twitter, forneça o username do usuário que será analisado e o termo desejado:

     $ pipenv run python main.py [screen_name] [termo]

Executando `pipenv run python main.py dan_abramov react` as funcionalidades providas pelo robô serão executadas para o usuário Dan Abramov em relação ao termo 'react'. As saídas dos algoritmos serão salvas no arquivo 'result.txt' na pasta raiz do projeto.

_O robô do Twitter está em um loop infinito, quando necessário deve-se interrompê-lo manualmente._


 ## Ativação do script
Com o script executando, sempre que novas menções são direcionadas à conta do Twitter associado às variáveis definidas acima, inicia-se a análise de cada menção individualmente.

_Por conta de limites da API, a verificação de novas menções ocorrem de 1 em 1 minuto._

Quando não há novas menções o script hiberna por 1 minutos, e verifica novamente novas menções.


## Análise das menções
A função _listener()_ é a primeira função a ser chamada no script. Ela é responsável pela coleta de novas menções, e determinar qual a próxima função a ser chamada de acordo com o conteúdo da menção. Para cada menção que é coletada, a string com seu conteúdo é quebrada, e verifica-se se o termo que o usuário utilizou. As opções padrões são limitadas ao uso dos termos QUEMSABE, QUANTOSSABEM e TERMOSMAISUSADOS.

A forma como será decidido qual fluxo seguir pode ser personalizada conforme o uso que será dado ao script.


 ## Quantos sabem
Essa análise foca em descobrir quantos amigos falaram sobre um termo.

É feita a coleta das publicações de quem o mencionador segue (amigos), que foram criadas até 7 dias precedentes ao início da análise e que possuem em seu conteúdo um termo especificado na menção. A função _how_many_knows(self, mention)_ busca quais amigos utilizaram o termo em seus tweets e faz uma contagem desses amigos.

Veja abaixo o diagrama de sequência que representa essa análise:
![alt text](https://preview.ibb.co/mvy4So/image1.jpg "Diagrama de Sequência - Quantos sabem")


 ## Quem sabe
Essa análise foca em descobrir quem é o melhor seguidor para responder algo sobre um termo.

É feita a coleta das publicações de quem segue o mencionador (seguidores), que foram criadas até 7 dias precedentes ao início da análise e que possuem em seu conteúdo um termo especificado na menção. A da função _who_knows(self, mention)_ busca quais seguidores utilizaram o termo em seus tweets. Em seguida, busca-se a publicação mais antiga, que servirá de referência para selecionar o melhor seguidor.

Para cada seguidor é feito o cálculo de uma pontuação que representa sua aptidão para responder alguma pergunta sobre o termo especificado. Sua pontuação aumenta a cada publicação que possui o termo, conforme a fórmula abaixo:

![alt text](https://preview.ibb.co/cRjaHo/image4.png "Fórmula - Quem sabe")

    - <b>Pw</b> é pontuação do seguidor w; 
    - <b>a</b> é publicação do seguidor w;  
    - <b>Tw,a</b> é o timestamp da publicação a; 
    - <b>T*</b> é o timestamp da publicação mais antiga
    - <b>now</b> é timestamp no momento da decisão de escalonamento (horário do sistema).

Ao final é retornado o seguidor com a melhor pontuação.
Veja abaixo o diagrama de sequência que representa essa análise:

![alt text](https://preview.ibb.co/dGL17o/image3.jpg "Diagrama de Sequência - Quem sabe")


## Termos mais usados
Essa análise foca em descobrir a frequência dos termos que aparecem na timeline do usuário.

É feita a coleta das publicações de quem o mencionador segue (amigos), que foram criadas até 7 dias precedentes ao início da análise e que possuem em seu conteúdo um termo especificado na menção. A função _most_used_terms(api, user_id, user_name)_ recupera os termos usados nas publicações e faz uma contagem destes.


## Respostas
Após a análise de cada menção, o mencionador é respondido, conforme o resultado opções dispiníveis no arquivo _mentions_replies.py_, podendo ser:

Para análise do tipo QUANTOSSABEM:

    - reply_mention_how_many(api, data, mention)

Para análise do tipo QUEMSABE:

    - reply_mention_who_know(api, data, mention)

Para análise do tipo TERMOSMAISUSADOS:

    - reply_mention_most_used_terms(api, data, mention)

Ou para menções em formato inválido:

    - reply_invalid_tweet(api, mention)
