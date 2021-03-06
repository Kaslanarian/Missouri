#ifndef OPENPOSE_GUI_W_ADD_GUI_INFO_HPP
#define OPENPOSE_GUI_W_ADD_GUI_INFO_HPP

#include <openpose/core/common.hpp>
#include <openpose/gui/guiInfoAdder.hpp>
#include <openpose/thread/worker.hpp>

namespace op
{
    template<typename TDatums>
    class WGuiInfoAdder : public Worker<TDatums>
    {
    public:
        explicit WGuiInfoAdder(const std::shared_ptr<GuiInfoAdder>& guiInfoAdder);

        virtual ~WGuiInfoAdder();

        void initializationOnThread();

        void work(TDatums& tDatums);

    private:
        std::shared_ptr<GuiInfoAdder> spGuiInfoAdder;

        DELETE_COPY(WGuiInfoAdder);
    };
}





// Implementation
#include <openpose/utilities/pointerContainer.hpp>
namespace op
{
    template<typename TDatums>
    WGuiInfoAdder<TDatums>::WGuiInfoAdder(const std::shared_ptr<GuiInfoAdder>& guiInfoAdder) :
        spGuiInfoAdder{guiInfoAdder}
    {
    }

    template<typename TDatums>
    WGuiInfoAdder<TDatums>::~WGuiInfoAdder()
    {
    }

    template<typename TDatums>
    void WGuiInfoAdder<TDatums>::initializationOnThread()
    {
    }

    template<typename TDatums>
    void WGuiInfoAdder<TDatums>::work(TDatums& tDatums)
    {
        try
        {
            if (checkNoNullNorEmpty(tDatums))
            {
                // Debugging log
                opLogIfDebug("", Priority::Low, __LINE__, __FUNCTION__, __FILE__);
                // Profiling speed
                const auto profilerKey = Profiler::timerInit(__LINE__, __FUNCTION__, __FILE__);
                // Add GUI components to frame
                for (auto& tDatumPtr : *tDatums)
                    spGuiInfoAdder->addInfo(
                        tDatumPtr->cvOutputData,
                        std::max(tDatumPtr->poseKeypoints.getSize(0), tDatumPtr->faceKeypoints.getSize(0)),
                        tDatumPtr->id, tDatumPtr->elementRendered.second, tDatumPtr->frameNumber,
                        tDatumPtr->poseIds, tDatumPtr->poseKeypoints);
                // Profiling speed
                Profiler::timerEnd(profilerKey);
                Profiler::printAveragedTimeMsOnIterationX(profilerKey, __LINE__, __FUNCTION__, __FILE__);
                // Debugging log
                opLogIfDebug("", Priority::Low, __LINE__, __FUNCTION__, __FILE__);
            }
        }
        catch (const std::exception& e)
        {
            this->stop();
            tDatums = nullptr;
            error(e.what(), __LINE__, __FUNCTION__, __FILE__);
        }
    }

    COMPILE_TEMPLATE_DATUM(WGuiInfoAdder);
}

#endif // OPENPOSE_GUI_W_ADD_GUI_INFO_HPP
