// eslint-disable-next-line @nrwl/nx/enforce-module-boundaries
import { FastifyInstance } from 'fastify';
import crypto from 'crypto';

const jobStatus: Record<string, number> = {};

function delay(seconds: number) {
  return new Promise((resolve) => {
    setTimeout(resolve, seconds * 1000);
  });
}

export default async function (fastify: FastifyInstance) {
  fastify.post('/upload-file', async (request, reply) => {
    reply.header('Access-Control-Allow-Origin', '*');
    reply.header('Access-Control-Allow-Methods', 'POST');
    // Logic to handle file upload goes here (omitted for brevity)

    const jobId = 'jija';
    jobStatus[jobId] = 0; // Initialize request count for this jobId
    return { jobId };
  });

  fastify.get('/task-status', async (request, reply) => {
    // @ts-ignore
    const jobId = request.query.jobId;

    reply.header('Access-Control-Allow-Origin', '*');
    reply.header('Access-Control-Allow-Methods', 'GET');

    await delay(3);

    if (!(jobId in jobStatus)) {
      jobStatus[jobId] = 0;
    }

    if (jobStatus[jobId] < 3) {
      jobStatus[jobId]++;
      return { complete: false };
    } else {
      const id = crypto.randomBytes(16).toString('hex');
      return { complete: true, id };
    }
  });

  fastify.get('/result-text', async (request, reply) => {
    reply.header('Access-Control-Allow-Origin', '*');
    reply.header('Access-Control-Allow-Methods', 'GET');

    // @ts-ignore
    const id = request.query.id;
    // Validate the ID and implement any additional logic if needed

    await delay(2);

    return {
      result: [
        {
          isDefinition: false,
          text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Tempor id eu nisl nunc mi ipsum faucibus. Pellentesque elit eget gravida cum sociis natoque penatibus et. Vel quam elementum pulvinar etiam non quam. Nulla pellentesque dignissim enim sit amet venenatis. Dolor sed viverra ipsum nunc aliquet. Egestas tellus rutrum tellus pellentesque eu tincidunt. Tristique senectus et netus et malesuada fames. Dolor sed viverra ipsum nunc aliquet bibendum enim facilisis gravida. Est ultricies integer quis auctor elit sed vulputate. Pharetra pharetra massa massa ultricies mi quis hendrerit dolor magna. Euismod elementum nisi quis eleifend quam. Dapibus ultrices in iaculis nunc sed augue.\nPhasellus egestas tellus rutrum tellus pellentesque. Laoreet suspendisse interdum consectetur libero. Sed viverra tellus in hac habitasse. In fermentum et sollicitudin ac orci. Sed viverra tellus in hac habitasse platea dictumst. Aenean pharetra magna ac placerat vestibulum lectus mauris. Nisi est sit amet facilisis. At risus viverra adipiscing at in tellus integer. Aliquet bibendum enim facilisis gravida neque convallis a. Erat velit scelerisque in dictum non consectetur. Lorem ',
        },
        {
          isDefinition: true,
          text: 'bebra',
        },
        {
          isDefinition: false,
          text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Est pellentesque elit ullamcorper dignissim cras tincidunt. Enim ut sem viverra aliquet eget sit. Rhoncus urna neque viverra justo nec ultrices dui sapien. Arcu odio ut sem nulla pharetra. Sit amet consectetur adipiscing elit pellentesque. Auctor augue mauris augue neque. Aliquam sem et tortor consequat id porta nibh venenatis. Ultrices eros in cursus turpis massa tincidunt dui ut. Lectus arcu bibendum at varius vel. Ultricies leo integer malesuada nunc vel risus. Erat imperdiet sed euismod nisi porta lorem mollis aliquam ut. Sociis natoque penatibus et magnis. Cursus sit amet dictum sit amet justo donec enim diam. Nibh mauris cursus mattis molestie a iaculis at erat. Mattis vulputate enim nulla aliquet porttitor lacus luctus accumsan. Amet dictum sit amet justo donec enim diam. Magna sit amet purus gravida quis blandit turpis.\nMaecenas volutpat blandit aliquam etiam erat velit scelerisque. In ante metus dictum at tempor commodo ullamcorper a lacus. Nisl nisi scelerisque eu ultrices vitae auctor. In massa tempor nec feugiat nisl pretium. At lectus urna duis convallis convallis. A erat nam at lectus urna duis. Mauris rhoncus aenean vel elit scelerisque. Risus in hendrerit gravida rutrum quisque non tellus orci ac. Fames ac turpis egestas integer eget aliquet nibh. Consectetur libero id faucibus nisl. Aliquam id diam maecenas ultricies mi eget mauris pharetra. Neque viverra justo nec ultrices dui. Lacus sed viverra tellus in hac habitasse. Arcu dictum varius duis ',
        },
        {
          isDefinition: true,
          text: 'WTF',
        },
        {
          isDefinition: false,
          text: '  sed do eiusmod tempor incididunt ut labore',
        },
      ],
      glossary: {
        bebra: 'Definition 1',
        WTF: 'More long definition, it includes one, two, three and urna neque viverra justo nec ultrices dui',
      },
    };
  });
}
