# Chain FAAS

## Intro
- Decentralized serverless platform
- It aims to address the growing energy consumption and carbon emissions associated with traditional data centers by leveraging the unused computational power of personal computers.

- Decentralized
- Blockchain based
- Leverages Excess computational power of personal computers
- Cost effective
- User friendly
- It can be used for running IoT applications closer to end-users.

## Background & Related Work
### Serverless Computing
- A Cloud computing model where the cloud provider automatically manages the infrastructure needed to run the code.
- Event based billing : (pay based on execution time)
- Autoscaling : Scales resources based on demand
- Container-based: Functions are executed in isolated containers for efficiency.
- (Disadvantage : Latency) : High latency

### Blockchain
- Records transactions across multiple computers in a decentralized & transparent manner.
- Identity can be public or private
- The blockchain itself can be public or private too
- Use consensus algorithms to validate transactions
- A consensus algorithm is a process used to achieve agreement on a single data value among distributed processes or systems.
- Bitcoin
- Hyperledger Fabric : A Blockchain platform suited for ChainFAAS
  - high transaction throughput
  - fast confirmation
  - support for smart contracts

### Related Work
#### Public Resource Computing
It utilizes idle processing power of personal computers for distributed computing. (BOINC and XtremWeb)
#### Blockchain-based Cloud Computing
iExec, Golem, and SONM
- It leverages blockchains for decentralized cloud computing on personal computers.
 