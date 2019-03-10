#ifndef TipPredict_DataFetcher_hpp
#define TipPredict_DataFetcher_hpp

#include "lbry/lbryapi.h"
#include <string>

using json = nlohmann::json;

namespace TipPredict
{

class DataFetcher
{
    private:
        std::string name;

    public:
        DataFetcher(std::string _name);

        void execute();

};

/* IMPLEMENTATIONS FOLLOW */
DataFetcher::DataFetcher(std::string _name)
:name(std::move(_name))
{

}

void DataFetcher::execute()
{
    json response = lbry::LbrydAPI::call(
                      "claim_list",             // method
                      {{"name", name}}  // param list as a std::map
                    );

    /* This returns a JSON-RPC formatted object in the form
        { 
            "id": "X",          // body values we sent to the API
            "jsonrpc": "2.0",   
            "result": {
                ...
                // this is the actual information  we received from the 
                // API. If something went wrong, instead of getting
                // "result" as the parent member, 
                // we'd instead get "error".
                ... 
            }
         } 
         */

    /* this prints out the request as a json-formatted object.
       in order to have it print correctly, use std::setw(4)
       to have it be formatted. The parameter to `std::setw()` 
       is the actual indentation value. Change it as you please.
    */

    // Simply call by the member name to get the body.
    json response_data = response["result"]["claims"];
    std::cout << std::setw(4) << response_data << std::endl;
}

} // namespace

#endif

